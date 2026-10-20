from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.core.limiter import limiter
from app.routers.auth import router as auth_router
from app.routers.cart import router as cart_router
from app.routers.dashboard import router as dashboard_router
from app.routers.orders import router as orders_router
from app.routers.products import categories_router, products_router
from app.routers.reviews import router as reviews_router
from app.routers.chat import router as chat_router
from app.routers.notifications import router as notifications_router
from app.routers.banners import router as banners_router

# Rate limiting
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

# Folder upload dibuat otomatis kalau belum ada
UPLOAD_DIR = Path(__file__).resolve().parents[1] / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

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
app.include_router(reviews_router, prefix=prefix)
app.include_router(cart_router, prefix=prefix)
app.include_router(orders_router, prefix=prefix)
app.include_router(dashboard_router, prefix=prefix)
app.include_router(chat_router, prefix=prefix)
app.include_router(notifications_router, prefix=prefix)
app.include_router(banners_router, prefix=prefix)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")


@app.get("/")
def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME} API", "docs": "/docs"}
