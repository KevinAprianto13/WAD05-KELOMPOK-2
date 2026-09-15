"""
Seed script: creates admin user, categories, and products.
Run: python -m app.db.seed
"""
from app.db.session import SessionLocal, engine
from app.models.models import Base, Cart, Category, Product, User, UserRole
from app.core.security import get_password_hash


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Admin user
    admin = db.query(User).filter(User.email == "admin@nusashop.com").first()
    if not admin:
        admin = User(
            email="admin@nusashop.com",
            full_name="Admin NusaShop",
            hashed_password=get_password_hash("admin123"),
            role=UserRole.admin,
        )
        db.add(admin)
        db.commit()
        print("[ OK ] Admin created: admin@nusashop.com / admin123")
    else:
        print("[ INFO ] Admin already exists")

    # Demo customer
    customer = db.query(User).filter(User.email == "customer@nusashop.com").first()
    if not customer:
        customer = User(
            email="customer@nusashop.com",
            full_name="Budi Santoso",
            hashed_password=get_password_hash("customer123"),
            role=UserRole.customer,
        )
        db.add(customer)
        db.commit()
        db.refresh(customer)
        cart = Cart(user_id=customer.id)
        db.add(cart)
        db.commit()
        print("[ OK ] Customer created: customer@nusashop.com / customer123")

    # Categories
    categories_data = [
        {"name": "Elektronik", "slug": "elektronik"},
        {"name": "Fashion", "slug": "fashion"},
        {"name": "Rumah & Dapur", "slug": "rumah-dapur"},
        {"name": "Olahraga", "slug": "olahraga"},
        {"name": "Kecantikan", "slug": "kecantikan"},
    ]
    cat_map = {}
    for cat_data in categories_data:
        cat = db.query(Category).filter(Category.slug == cat_data["slug"]).first()
        if not cat:
            cat = Category(**cat_data)
            db.add(cat)
            db.commit()
            db.refresh(cat)
        cat_map[cat_data["slug"]] = cat.id

    print("[ OK ] Categories seeded")

    # Products
    products_data = [
        {
            "name": "Laptop Gaming ASUS ROG",
            "description": "Laptop gaming performa tinggi dengan RTX 4060, RAM 16GB, SSD 512GB. Cocok untuk gaming dan desain grafis.",
            "price": 15999000,
            "stock": 20,
            "image_url": "https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=500",
            "category_id": cat_map["elektronik"],
        },
        {
            "name": "Smartphone Samsung Galaxy S24",
            "description": "Flagship terbaru Samsung dengan kamera 200MP, layar Dynamic AMOLED 2X, dan baterai 5000mAh.",
            "price": 12499000,
            "stock": 35,
            "image_url": "https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=500",
            "category_id": cat_map["elektronik"],
        },
        {
            "name": "Headphone Sony WH-1000XM5",
            "description": "Headphone premium dengan noise cancellation terbaik di kelasnya. Suara jernih dan bass yang dalam.",
            "price": 4299000,
            "stock": 50,
            "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500",
            "category_id": cat_map["elektronik"],
        },
        {
            "name": "Smartwatch Apple Watch Series 9",
            "description": "Smartwatch canggih dengan fitur health monitoring, GPS, dan layar always-on retina display.",
            "price": 6999000,
            "stock": 25,
            "image_url": "https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=500",
            "category_id": cat_map["elektronik"],
        },
        {
            "name": "Kemeja Batik Premium Pria",
            "description": "Kemeja batik motif parang dengan bahan katun premium. Cocok untuk formal maupun casual.",
            "price": 299000,
            "stock": 100,
            "image_url": "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=500",
            "category_id": cat_map["fashion"],
        },
        {
            "name": "Sneakers Nike Air Max",
            "description": "Sepatu sneakers kasual dengan teknologi Air Max untuk kenyamanan maksimal sepanjang hari.",
            "price": 1299000,
            "stock": 60,
            "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500",
            "category_id": cat_map["fashion"],
        },
        {
            "name": "Tas Ransel Laptop",
            "description": "Ransel anti air dengan kompartemen laptop 15 inch, port USB charging, dan desain ergonomis.",
            "price": 459000,
            "stock": 80,
            "image_url": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=500",
            "category_id": cat_map["fashion"],
        },
        {
            "name": "Rice Cooker Cosmos 2 Liter",
            "description": "Rice cooker digital dengan timer, fungsi warm otomatis, dan anti lengket premium.",
            "price": 389000,
            "stock": 45,
            "image_url": "https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=500",
            "category_id": cat_map["rumah-dapur"],
        },
        {
            "name": "Blender Philips 2L",
            "description": "Blender kuat 800W dengan jar kaca 2L. Cocok untuk smoothie, jus, dan makanan bayi.",
            "price": 549000,
            "stock": 30,
            "image_url": "https://images.unsplash.com/photo-1570222094114-d054a817e56b?w=500",
            "category_id": cat_map["rumah-dapur"],
        },
        {
            "name": "Dumbbell Set 10-30kg",
            "description": "Set dumbbell adjustable berkualitas tinggi untuk latihan di rumah. Dilengkapi rack penyimpanan.",
            "price": 1899000,
            "stock": 15,
            "image_url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=500",
            "category_id": cat_map["olahraga"],
        },
        {
            "name": "Sepatu Lari Adidas Ultraboost",
            "description": "Sepatu lari teknologi Boost untuk kenyamanan dan performa terbaik. Tersedia berbagai ukuran.",
            "price": 2199000,
            "stock": 40,
            "image_url": "https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=500",
            "category_id": cat_map["olahraga"],
        },
        {
            "name": "Serum Vitamin C Wardah",
            "description": "Serum vitamin C brightening untuk kulit cerah dan bebas flek hitam. Cocok untuk semua jenis kulit.",
            "price": 89000,
            "stock": 200,
            "image_url": "https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=500",
            "category_id": cat_map["kecantikan"],
        },
    ]

    for prod_data in products_data:
        existing = db.query(Product).filter(Product.name == prod_data["name"]).first()
        if not existing:
            product = Product(**prod_data)
            db.add(product)

    db.commit()
    print(f"[ OK ] {len(products_data)} products seeded")
    db.close()
    print("\nSeed complete! Login with:")
    print("   Admin: admin@nusashop.com / admin123")
    print("   Customer: customer@nusashop.com / customer123")


if __name__ == "__main__":
    seed()
