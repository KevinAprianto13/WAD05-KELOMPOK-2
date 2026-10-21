# Panduan Deploy NusaShop ke Vercel & Neon PostgreSQL

Dokumen ini berisi panduan lengkap langkah demi langkah untuk mendeploy aplikasi NusaShop (FastAPI + Vue 3) ke **Vercel** dengan database PostgreSQL di **Neon**.

---

## 1. Siapkan Database di Neon (Gratis)

1. Buka [neon.tech](https://neon.tech) lalu login / register akun.
2. Buat Project baru, misalnya beri nama `nusashop`.
3. Pada halaman dashboard project, lihat bagian **Connection Details**.
4. Salin **Connection String**, contohnya:
   ```text
   postgresql://neondb_owner:npg_xxxx@ep-cool-butterfly-12345.us-east-2.aws.neon.tech/neondb?sslmode=require
   ```
   *(Catatan: Backend sudah otomatis menyesuaikan format string ini ke driver SQLAlchemy `postgresql+psycopg://`)*.

---

## 2. Commit dan Push Kode ke GitHub

Pastikan semua file konfigurasi deployment sudah ter-commit dan di-push ke repository GitHub:

```bash
git add .
git commit -m "feat: konfigurasi deployment vercel serverless dan neon postgresql"
git push origin main
```

---

## 3. Deploy ke Vercel

1. Buka [vercel.com](https://vercel.com) dan login dengan akun GitHub Anda.
2. Klik tombol **Add New...** -> **Project**.
3. Cari dan pilih repository **`KevinAprianto13/WAD05-KELOMPOK-2`**, lalu klik **Import**.
4. Pengaturan project:
   - **Framework Preset**: biarkan default / Vite
   - **Root Directory**: `./` (biarkan default root)
5. Buka bagian **Environment Variables** dan tambahkan dua variabel berikut:
   | Key | Value | Keterangan |
   | --- | --- | --- |
   | `DATABASE_URL` | *(Connection String dari Neon di langkah 1)* | URL database PostgreSQL Neon |
   | `SECRET_KEY` | `nusashop-jwt-secret-key-produksi-bebas-diisi-apa-saja` | Kunci enkripsi token login JWT |
6. Klik tombol **Deploy** dan tunggu proses build selesai (sekitar 1–2 menit).

---

## 4. Inisialisasi Database (Migrasi & Data Awal)

Setelah deployment di Vercel selesai dan berstatus **Ready**:

1. Buka URL domain Vercel Anda dengan endpoint `/api/v1/init-db` di browser:
   ```text
   https://<nama-project-anda>.vercel.app/api/v1/init-db
   ```
2. Halaman akan menampilkan respon JSON:
   ```json
   {
     "status": "success",
     "message": "Database Neon berhasil diinisialisasi dan data awal (Admin & Produk) telah di-seed!",
     "admin": "admin@nusashop.com / admin123",
     "customer": "customer@nusashop.com / customer123"
   }
   ```
3. Endpoint ini secara otomatis:
   - Menjalankan migrasi database Alembic untuk membuat seluruh tabel di Neon.
   - Mengisi akun Admin default (`admin@nusashop.com`).
   - Mengisi akun Customer demo (`customer@nusashop.com`).
   - Mengisi 5 kategori produk dan 12 data produk awal.

---

## 5. Buka Aplikasi

Kunjungi alamat utama website Anda:
```text
https://<nama-project-anda>.vercel.app
```

Anda sudah bisa login dengan:
- **Admin**: `admin@nusashop.com` / `admin123` (mengelola produk, banner, pesanan, dan chat admin)
- **Customer**: `customer@nusashop.com` / `customer123` (berbelanja, keranjang, checkout, ulasan produk)
- Dokumentasi API Swagger: `https://<nama-project-anda>.vercel.app/docs`
