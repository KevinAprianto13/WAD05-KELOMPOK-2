from typing import Optional
from datetime import datetime

from pydantic import BaseModel, EmailStr


# ── Auth Schemas ──────────────────────────────────────────────────────────────

class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str


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
    name: str
    slug: str


class CategoryOut(BaseModel):
    id: int
    name: str
    slug: str

    class Config:
        from_attributes = True


# ── Product Schemas ───────────────────────────────────────────────────────────

class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int = 0
    image_url: Optional[str] = None
    category_id: Optional[int] = None


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
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
    quantity: int = 1


class CartItemUpdate(BaseModel):
    quantity: int


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
    shipping_address: str
    notes: Optional[str] = None
    payment_method: str = "transfer"


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
    receiver_id: int
    content: str


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
