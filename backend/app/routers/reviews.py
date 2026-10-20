from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.models import Order, OrderItem, OrderStatus, Product, Review, User, UserRole
from app.schemas.schemas import ReviewCreate, ReviewOut

router = APIRouter(prefix="/products", tags=["reviews"])


@router.get("/{product_id}/reviews", response_model=List[ReviewOut])
def list_reviews(product_id: int, db: Session = Depends(get_db)):
    return (
        db.query(Review)
        .filter(Review.product_id == product_id)
        .order_by(Review.created_at.desc())
        .all()
    )


@router.post("/{product_id}/reviews", response_model=ReviewOut, status_code=201)
def create_review(
    product_id: int,
    review_in: ReviewCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.role != UserRole.customer:
        raise HTTPException(status_code=403, detail="Hanya customer yang bisa memberi ulasan")

    product = db.query(Product).filter(Product.id == product_id, Product.is_active == True).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Hanya pembeli yang pesanannya sudah diterima (delivered) yang boleh memberi ulasan
    pernah_beli = (
        db.query(OrderItem)
        .join(Order)
        .filter(
            Order.user_id == current_user.id,
            Order.status == OrderStatus.delivered,
            OrderItem.product_id == product_id,
        )
        .first()
    )
    if not pernah_beli:
        raise HTTPException(
            status_code=403,
            detail="Ulasan hanya bisa diberikan setelah pesanan produk ini diterima",
        )

    sudah_review = db.query(Review).filter(
        Review.user_id == current_user.id, Review.product_id == product_id
    ).first()
    if sudah_review:
        raise HTTPException(status_code=409, detail="Kamu sudah memberi ulasan untuk produk ini")

    review = Review(
        user_id=current_user.id,
        product_id=product_id,
        rating=review_in.rating,
        comment=review_in.comment,
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review
