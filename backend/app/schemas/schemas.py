from typing import Literal, Optional
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


# ── Auth Schemas ──────────────────────────────────────────────────────────────

class UserCreate(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=2, max_length=100)
    password: str = Field(min_length=8, max_length=72)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: str
    full_name: str
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


# ── Category Schemas ──────────────────────────────────────────────────────────

class CategoryCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    slug: str = Field(min_length=2, max_length=50, pattern=r"^[a-z0-9-]+$")


class CategoryOut(BaseModel):
    id: int
    name: str
    slug: str

    class Config:
        from_attributes = True


# ── Product Schemas ───────────────────────────────────────────────────────────

class ProductCreate(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    description: Optional[str] = None
    price: float = Field(gt=0)
    stock: int = Field(0, ge=0)
    image_url: Optional[str] = None
    category_id: Optional[int] = None


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=150)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    image_url: Optional[str] = None
    category_id: Optional[int] = None
    is_active: Optional[bool] = None


class ProductImageOut(BaseModel):
    id: int
    image_url: str
    sort_order: int

    class Config:
        from_attributes = True


class ProductOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    stock: int
    image_url: Optional[str]
    is_active: bool
    category_id: Optional[int]
    category: Optional[CategoryOut]
    images: list[ProductImageOut] = []
    created_at: datetime

    class Config:
        from_attributes = True


# ── Cart Schemas ──────────────────────────────────────────────────────────────

class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(1, gt=0, le=100)


class CartItemUpdate(BaseModel):
    quantity: int = Field(ge=0, le=100)


class CartItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    product: ProductOut

    class Config:
        from_attributes = True


class CartOut(BaseModel):
    id: int
    items: list[CartItemOut]

    class Config:
        from_attributes = True


# ── Order Schemas ─────────────────────────────────────────────────────────────

class CheckoutRequest(BaseModel):
    shipping_address: str = Field(min_length=10, max_length=500)
    notes: Optional[str] = Field(None, max_length=500)
    payment_method: Literal["transfer", "gopay", "ovo", "qris"] = "transfer"


class OrderItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: float
    product: ProductOut

    class Config:
        from_attributes = True


class PaymentOut(BaseModel):
    id: int
    status: str
    method: str
    created_at: datetime

    class Config:
        from_attributes = True


class OrderOut(BaseModel):
    id: int
    status: str
    total_price: float
    shipping_address: str
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    items: list[OrderItemOut]
    payment: Optional[PaymentOut]
    user: Optional[UserOut]

    class Config:
        from_attributes = True


class OrderStatusUpdate(BaseModel):
    status: str


# ── Dashboard Schemas ─────────────────────────────────────────────────────────

class DashboardStats(BaseModel):
    total_revenue: float
    total_orders: int
    total_customers: int
    total_products: int
    pending_orders: int


class SalesDataPoint(BaseModel):
    date: str
    revenue: float
    orders: int


# ── Chat Schemas ──────────────────────────────────────────────────────────────

class ChatMessageCreate(BaseModel):
    receiver_id: int = 0
    content: str = Field(min_length=1, max_length=1000)


class ChatMessageOut(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    content: str
    is_read: bool
    created_at: datetime
    sender: Optional[UserOut] = None

    class Config:
        from_attributes = True


class ChatSessionOut(BaseModel):
    user: UserOut
    last_message: ChatMessageOut
    unread_count: int


# ── Notification Schemas ──────────────────────────────────────────────────────

class NotificationOut(BaseModel):
    id: int
    user_id: int
    title: str
    message: str
    type: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True
