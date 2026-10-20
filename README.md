# NusaShop

Aplikasi e-commerce mini untuk Group Project Web Application Development (WAD05) Kelompok 2.

- Frontend: Vue 3, Vite, Pinia, Vue Router
- Backend: FastAPI, SQLAlchemy, Alembic
- Database: PostgreSQL
- CI: GitHub Actions (pytest + build frontend)

## Yang perlu di-install

- Python 3.10 atau lebih baru
- Node.js 20.19 atau lebih baru
- PostgreSQL 14 atau lebih baru

## 1. Siapkan database

Buat user dan database di PostgreSQL:

```sql
CREATE USER nusashop WITH PASSWORD 'nusashop';
CREATE DATABASE nusashop OWNER nusashop;
```

## 2. Jalankan backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # lalu ganti SECRET_KEY
alembic upgrade head             # membuat semua tabel
python -m app.db.seed            # mengisi data awal
uvicorn app.main:app --reload
```

Backend berjalan di http://localhost:8000 dan dokumentasi API ada di http://localhost:8000/docs.

## 3. Jalankan frontend

Buka terminal baru:

```bash
cd frontend
npm install
npm run dev
```

Buka http://localhost:5173.

## Akun demo

| Peran | Email | Password |
| --- | --- | --- |
| Admin | admin@nusashop.com | admin123 |
| Customer | customer@nusashop.com | customer123 |

Akun admin hanya dibuat lewat seed. Registrasi dari halaman web selalu menjadi customer.

## Menjalankan test

Test memakai database terpisah supaya data development tidak terhapus.

```sql
CREATE DATABASE nusashop_test OWNER nusashop;
```

```bash
cd backend
pip install -r requirements-dev.txt
DATABASE_URL=postgresql+psycopg://nusashop:nusashop@localhost:5432/nusashop_test pytest -v
```

## Catatan

- Pembayaran hanya simulasi. Status pembayaran langsung `paid` saat checkout, tanpa payment gateway.
- Notifikasi dan chat diperbarui dengan polling, bukan WebSocket.
