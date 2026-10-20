from pathlib import Path
from typing import List, Optional
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from PIL import Image, ImageOps, UnidentifiedImageError
from sqlalchemy.orm import Session, joinedload

from app.core.deps import get_current_admin
from app.db.session import get_db
from app.models.models import Category, Product, ProductImage
from app.schemas.schemas import CategoryCreate, CategoryOut, ProductCreate, ProductOut, ProductUpdate

# ── Categories ────────────────────────────────────────────────────────────────

categories_router = APIRouter(prefix="/categories", tags=["categories"])


@categories_router.get("", response_model=List[CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()


@categories_router.post("", response_model=CategoryOut, status_code=201)
def create_category(cat_in: CategoryCreate, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    existing = db.query(Category).filter(Category.slug == cat_in.slug).first()
    if existing:
        raise HTTPException(status_code=400, detail="Category slug already exists")
    cat = Category(**cat_in.model_dump())
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat


@categories_router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    cat = db.query(Category).filter(Category.id == category_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    if db.query(Product).filter(Product.category_id == category_id).first():
        raise HTTPException(status_code=400, detail="Kategori masih dipakai oleh produk")
    db.delete(cat)
    db.commit()
    return {"message": "Category deleted"}


# ── Products ──────────────────────────────────────────────────────────────────

products_router = APIRouter(prefix="/products", tags=["products"])
PRODUCT_UPLOAD_DIR = Path(__file__).resolve().parents[2] / "uploads" / "products"
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}


@products_router.get("", response_model=List[ProductOut])
def list_products(
    search: Optional[str] = Query(None),
    category_id: Optional[int] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    q = db.query(Product).options(joinedload(Product.category)).filter(Product.is_active == True)
    if search:
        q = q.filter(Product.name.ilike(f"%{search}%"))
    if category_id:
        q = q.filter(Product.category_id == category_id)
    if min_price is not None:
        q = q.filter(Product.price >= min_price)
    if max_price is not None:
        q = q.filter(Product.price <= max_price)
    return q.offset(skip).limit(limit).all()


@products_router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = (
        db.query(Product)
        .options(joinedload(Product.category))
        .filter(Product.id == product_id, Product.is_active == True)
        .first()
    )
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@products_router.post("", response_model=ProductOut, status_code=201)
def create_product(product_in: ProductCreate, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    product = Product(**product_in.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    # Reload with category
    return db.query(Product).options(joinedload(Product.category)).filter(Product.id == product.id).first()


@products_router.put("/{product_id}", response_model=ProductOut)
def update_product(
    product_id: int,
    product_in: ProductUpdate,
    db: Session = Depends(get_db),
    _=Depends(get_current_admin),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    for field, value in product_in.model_dump(exclude_unset=True).items():
        setattr(product, field, value)
    db.commit()
    db.refresh(product)
    return db.query(Product).options(joinedload(Product.category)).filter(Product.id == product_id).first()


@products_router.post("/{product_id}/image", response_model=ProductOut)
async def upload_product_image(
    product_id: int,
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    _=Depends(get_current_admin),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if image.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=400, detail="Gunakan gambar JPG, PNG, atau WebP")

    content = await image.read()
    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Ukuran gambar maksimal 10 MB")
    try:
        from io import BytesIO
        source = Image.open(BytesIO(content)).convert("RGB")
        fitted = ImageOps.fit(source, (800, 800), method=Image.Resampling.LANCZOS)
    except (UnidentifiedImageError, OSError):
        raise HTTPException(status_code=400, detail="File gambar tidak dapat dibaca")

    PRODUCT_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"product-{product_id}-{uuid4().hex}.webp"
    fitted.save(PRODUCT_UPLOAD_DIR / filename, format="WEBP", quality=88, method=6)
    product.image_url = f"/uploads/products/{filename}"
    db.commit()
    return db.query(Product).options(joinedload(Product.category)).filter(Product.id == product_id).first()


@products_router.post("/{product_id}/images", response_model=ProductOut)
async def upload_product_images(
    product_id: int,
    images: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    _=Depends(get_current_admin),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if not images or len(images) > 10:
        raise HTTPException(status_code=400, detail="Upload 1 sampai 10 gambar")

    PRODUCT_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    next_order = db.query(ProductImage).filter(ProductImage.product_id == product_id).count()
    for image in images:
        if image.content_type not in ALLOWED_IMAGE_TYPES:
            raise HTTPException(status_code=400, detail="Gunakan gambar JPG, PNG, atau WebP")
        content = await image.read()
        if len(content) > 10 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="Ukuran setiap gambar maksimal 10 MB")
        try:
            from io import BytesIO
            source = Image.open(BytesIO(content)).convert("RGB")
            fitted = ImageOps.fit(source, (800, 800), method=Image.Resampling.LANCZOS)
        except (UnidentifiedImageError, OSError):
            raise HTTPException(status_code=400, detail="File gambar tidak dapat dibaca")
        filename = f"product-{product_id}-{uuid4().hex}.webp"
        fitted.save(PRODUCT_UPLOAD_DIR / filename, format="WEBP", quality=88, method=6)
        db.add(ProductImage(product_id=product_id, image_url=f"/uploads/products/{filename}", sort_order=next_order))
        next_order += 1
    db.commit()
    return db.query(Product).options(joinedload(Product.category)).filter(Product.id == product_id).first()


@products_router.delete("/{product_id}/images/{image_id}", response_model=ProductOut)
def delete_product_image(
    product_id: int,
    image_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_admin),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    image = db.query(ProductImage).filter(ProductImage.id == image_id, ProductImage.product_id == product_id).first()
    if not product or not image:
        raise HTTPException(status_code=404, detail="Gambar produk tidak ditemukan")
    db.delete(image)
    db.commit()
    return db.query(Product).options(joinedload(Product.category)).filter(Product.id == product_id).first()


@products_router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product.is_active = False
    db.commit()
    return {"message": "Product deactivated"}
