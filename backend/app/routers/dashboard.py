from datetime import datetime, timedelta, timezone
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.deps import get_current_admin
from app.db.session import get_db
from app.models.models import Order, OrderItem, OrderStatus, Product, User
from app.schemas.schemas import DashboardStats, SalesDataPoint

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/dashboard/stats", response_model=DashboardStats)
def get_dashboard_stats(_=Depends(get_current_admin), db: Session = Depends(get_db)):
    total_revenue = db.query(func.sum(Order.total_price)).filter(
        Order.status != OrderStatus.cancelled
    ).scalar() or 0.0

    total_orders = db.query(func.count(Order.id)).scalar() or 0
    total_customers = db.query(func.count(User.id)).scalar() or 0
    total_products = db.query(func.count(Product.id)).filter(Product.is_active == True).scalar() or 0
    pending_orders = db.query(func.count(Order.id)).filter(Order.status == OrderStatus.pending).scalar() or 0

    return DashboardStats(
        total_revenue=total_revenue,
        total_orders=total_orders,
        total_customers=total_customers,
        total_products=total_products,
        pending_orders=pending_orders,
    )


@router.get("/dashboard/sales", response_model=List[SalesDataPoint])
def get_sales_chart(_=Depends(get_current_admin), db: Session = Depends(get_db)):
    """Returns daily sales data for the last 30 days"""
    result = []
    today = datetime.now(timezone.utc).date()

    for i in range(29, -1, -1):
        day = today - timedelta(days=i)
        day_start = datetime.combine(day, datetime.min.time()).replace(tzinfo=timezone.utc)
        day_end = day_start + timedelta(days=1)

        orders_on_day = (
            db.query(Order)
            .filter(
                Order.created_at >= day_start,
                Order.created_at < day_end,
                Order.status != OrderStatus.cancelled,
            )
            .all()
        )

        revenue = sum(o.total_price for o in orders_on_day)
        result.append(
            SalesDataPoint(
                date=day.strftime("%Y-%m-%d"),
                revenue=revenue,
                orders=len(orders_on_day),
            )
        )

    return result
