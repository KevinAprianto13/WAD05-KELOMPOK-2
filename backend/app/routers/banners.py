from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from urllib.request import Request, urlopen
from sqlalchemy.orm import Session
from PIL import Image, ImageOps, UnidentifiedImageError

from app.core.deps import get_current_admin
from app.db.session import get_db
from app.models.models import Banner
from app.schemas.banner import BannerResponse

router = APIRouter(prefix="/banners", tags=["banners"])
UPLOAD_DIR = Path(__file__).resolve().parents[2] / "uploads" / "banners"
SLOT_SIZES = {"main": (1600, 886), "side_1": (1200, 625), "side_2": (1200, 625)}
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_UPLOAD_BYTES = 10 * 1024 * 1024


@router.get("", response_model=list[BannerResponse])
def list_banners(db: Session = Depends(get_db)):
    return db.query(Banner).filter(Banner.is_active == True).order_by(Banner.id).all()


@router.post("/{position}", response_model=BannerResponse)
async def upload_banner(
    position: str,
    image: UploadFile | None = File(None),
    image_url: str | None = Form(None),
    title: str | None = Form(None),
    subtitle: str | None = Form(None),
    link_url: str | None = Form(None),
    db: Session = Depends(get_db),
    _=Depends(get_current_admin),
):
    if position not in SLOT_SIZES:
        raise HTTPException(status_code=400, detail="Posisi banner tidak valid")

    banner = db.query(Banner).filter(Banner.position == position).first()
    if not image and not image_url and not banner:
        raise HTTPException(status_code=400, detail="Pilih file gambar atau masukkan URL gambar")

    if not image and not image_url and banner:
        banner.title = title
        banner.subtitle = subtitle
        banner.link_url = link_url
        banner.is_active = True
        db.commit()
        db.refresh(banner)
        return banner

    if image:
        if image.content_type not in ALLOWED_TYPES:
            raise HTTPException(status_code=400, detail="Gunakan gambar JPG, PNG, atau WebP")
        content = await image.read()
    else:
        try:
            request = Request(image_url, headers={"User-Agent": "NusaShop/1.0"})
            with urlopen(request, timeout=10) as response:
                content = response.read(MAX_UPLOAD_BYTES + 1)
        except Exception:
            raise HTTPException(status_code=400, detail="URL gambar tidak dapat diakses")

    if len(content) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=400, detail="Ukuran gambar maksimal 10 MB")

    try:
        from io import BytesIO
        source = Image.open(BytesIO(content)).convert("RGB")
        fitted = ImageOps.fit(source, SLOT_SIZES[position], method=Image.Resampling.LANCZOS)
    except (UnidentifiedImageError, OSError):
        raise HTTPException(status_code=400, detail="File gambar tidak dapat dibaca")

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"{position}-{uuid4().hex}.webp"
    output_path = UPLOAD_DIR / filename
    fitted.save(output_path, format="WEBP", quality=88, method=6)

    if not banner:
        banner = Banner(position=position)
        db.add(banner)
    banner.title = title
    banner.subtitle = subtitle
    banner.link_url = link_url
    banner.image_url = f"/uploads/banners/{filename}"
    banner.is_active = True
    db.commit()
    db.refresh(banner)
    return banner


@router.delete("/{position}")
def delete_banner(position: str, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    banner = db.query(Banner).filter(Banner.position == position).first()
    if not banner:
        raise HTTPException(status_code=404, detail="Banner tidak ditemukan")
    banner.is_active = False
    db.commit()
    return {"message": "Banner dihapus"}