import pytest
from fastapi.testclient import TestClient

from app.core.limiter import limiter
from app.core.security import get_password_hash
from app.db.session import Base, SessionLocal, engine
from app.main import app
from app.models.models import Category, Product, User, UserRole


@pytest.fixture(autouse=True)
def database():
    # Setiap test mulai dari database kosong
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    limiter.reset()

    db = SessionLocal()
    db.add(User(email="admin@test.com", full_name="Admin Test",
                hashed_password=get_password_hash("admin12345"), role=UserRole.admin))
    category = Category(name="Elektronik", slug="elektronik")
    db.add(category)
    db.commit()
    db.add(Product(name="Mouse Wireless", price=150000, stock=10, category_id=category.id))
    db.commit()
    db.close()
    yield


@pytest.fixture
def client():
    return TestClient(app)


def login(client, email, password):
    res = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    return {"Authorization": f"Bearer {res.json()['access_token']}"}


def register(client, email="budi@test.com", password="budi12345"):
    client.post("/api/v1/auth/register", json={"email": email, "full_name": "Budi", "password": password})
    return login(client, email, password)


@pytest.fixture
def admin_headers(client):
    return login(client, "admin@test.com", "admin12345")


@pytest.fixture
def customer_headers(client):
    return register(client)
