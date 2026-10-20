from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.core.deps import get_current_admin, get_current_user
from app.db.session import get_db
from app.models.models import (Cart, CartItem, Order, OrderItem, OrderStatus,
                               Payment, PaymentStatus, Product, User, Notification, UserRole)
from app.schemas.schemas import CheckoutRequest, OrderOut, OrderStatusUpdate

router = APIRouter(prefix="/orders", tags=["orders"])

# Status yang boleh dituju dari status sekarang
NEXT_STATUS = {
    OrderStatus.pending: [OrderStatus.processing, OrderStatus.cancelled],
    OrderStatus.processing: [OrderStatus.shipped, OrderStatus.cancelled],
    OrderStatus.shipped: [OrderStatus.delivered],
    OrderStatus.delivered: [],
    OrderStatus.cancelled: [],
}


@router.post("/checkout", response_model=OrderOut, status_code=201)
def checkout(
    checkout_in: CheckoutRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    cart = (
        db.query(Cart)
        .options(joinedload(Cart.items).joinedload(CartItem.product))
        .filter(Cart.user_id == current_user.id)
        .first()
    )

    if not cart or not cart.items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    # Kunci baris produk supaya dua checkout bersamaan tidak membuat stok minus
    product_ids = [item.product_id for item in cart.items]
    db.query(Product).filter(Product.id.in_(product_ids)).order_by(Product.id).with_for_update().all()

    # Validate stock & calculate total
    total = 0
    for item in cart.items:
        db.refresh(item.product)
        if not item.product.is_active:
            raise HTTPException(status_code=400, detail=f"Produk {item.product.name} sudah tidak dijual")
        if item.product.stock < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for product: {item.product.name}",
            )
        total += item.product.price * item.quantity

    # Create order
    order = Order(
        user_id=current_user.id,
        total_price=total,
        shipping_address=checkout_in.shipping_address,
        notes=checkout_in.notes,
        status=OrderStatus.pending,
    )
    db.add(order)
    db.flush()

    # Create order items & reduce stock
    for item in cart.items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=item.product.price,
        )
        db.add(order_item)
        item.product.stock -= item.quantity

    # Create payment record
    payment = Payment(
        order_id=order.id,
        status=PaymentStatus.paid,  # Auto-paid for demo
        method=checkout_in.payment_method,
    )
    db.add(payment)

    # Clear cart
    db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
    
    # Notify all admins
    admins = db.query(User).filter(User.role == "admin").all()
    for admin in admins:
        notif = Notification(
            user_id=admin.id,
            title="Pesanan Baru",
            message=f"Ada pesanan baru #{order.id} senilai Rp {total:,.0f}.",
            type="order"
        )
        db.add(notif)
        
    db.commit()

    return (
        db.query(Order)
        .options(
            joinedload(Order.items).joinedload(OrderItem.product).joinedload(Product.category),
            joinedload(Order.payment),
            joinedload(Order.user),
        )
        .filter(Order.id == order.id)
        .first()
    )


@router.get("/me", response_model=List[OrderOut])
def get_my_orders(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return (
        db.query(Order)
        .options(
            joinedload(Order.items).joinedload(OrderItem.product).joinedload(Product.category),
            joinedload(Order.payment),
            joinedload(Order.user),
        )
        .filter(Order.user_id == current_user.id)
        .order_by(Order.created_at.desc())
        .all()
    )


@router.get("", response_model=List[OrderOut])
def get_all_orders(
    _: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    return (
        db.query(Order)
        .options(
            joinedload(Order.items).joinedload(OrderItem.product).joinedload(Product.category),
            joinedload(Order.payment),
            joinedload(Order.user),
        )
        .order_by(Order.created_at.desc())
        .all()
    )


@router.put("/{order_id}/status", response_model=OrderOut)
def update_order_status(
    order_id: int,
    status_in: OrderStatusUpdate,
    _: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    try:
        new_status = OrderStatus(status_in.status)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid status: {status_in.status}")

    if new_status not in NEXT_STATUS[order.status]:
        raise HTTPException(
            status_code=400,
            detail=f"Status tidak bisa diubah dari {order.status.value} ke {new_status.value}",
        )

    # Pesanan batal, stok dikembalikan
    if new_status == OrderStatus.cancelled:
        for item in order.items:
            item.product.stock += item.quantity

    order.status = new_status

    # Notify customer
    notif = Notification(
        user_id=order.user_id,
        title="Status Pesanan Diperbarui",
        message=f"Status pesanan #{order.id} Anda telah diubah menjadi: {order.status.value.upper()}.",
        type="order"
    )
    db.add(notif)

    db.commit()
    return (
        db.query(Order)
        .options(
            joinedload(Order.items).joinedload(OrderItem.product).joinedload(Product.category),
            joinedload(Order.payment),
            joinedload(Order.user),
        )
        .filter(Order.id == order_id)
        .first()
    )
