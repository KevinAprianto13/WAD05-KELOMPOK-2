from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.db.session import engine
from app.models.models import Base
from app.routers.auth import router as auth_router
from app.routers.cart import router as cart_router
from app.routers.dashboard import router as dashboard_router
from app.routers.orders import router as orders_router
from app.routers.products import categories_router, products_router
from app.routers.chat import router as chat_router
from app.routers.notifications import router as notifications_router
from app.routers.banners import router as banners_router

# Rate limiting
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="NusaShop E-commerce REST API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
prefix = settings.API_V1_STR
app.include_router(auth_router, prefix=prefix)
app.include_router(products_router, prefix=prefix)
app.include_router(categories_router, prefix=prefix)
app.include_router(cart_router, prefix=prefix)
app.include_router(orders_router, prefix=prefix)
app.include_router(dashboard_router, prefix=prefix)
app.include_router(chat_router, prefix=prefix)
app.include_router(notifications_router, prefix=prefix)
app.include_router(banners_router, prefix=prefix)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


@app.get("/")
def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME} API", "docs": "/docs"}
