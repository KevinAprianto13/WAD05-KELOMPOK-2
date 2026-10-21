API = "/api/v1"
ALAMAT = {"shipping_address": "Jl. Merdeka No. 10, Jakarta"}


def beli_sampai_diterima(client, customer_headers, admin_headers):
    client.post(f"{API}/cart/items", json={"product_id": 1, "quantity": 1}, headers=customer_headers)
    order_id = client.post(f"{API}/orders/checkout", json=ALAMAT, headers=customer_headers).json()["id"]
    for status in ["processing", "shipped", "delivered"]:
        client.put(f"{API}/orders/{order_id}/status", json={"status": status}, headers=admin_headers)


def test_belum_beli_tidak_bisa_review(client, customer_headers):
    res = client.post(f"{API}/products/1/reviews", json={"rating": 5}, headers=customer_headers)
    assert res.status_code == 403


def test_pesanan_belum_diterima_tidak_bisa_review(client, customer_headers):
    client.post(f"{API}/cart/items", json={"product_id": 1, "quantity": 1}, headers=customer_headers)
    client.post(f"{API}/orders/checkout", json=ALAMAT, headers=customer_headers)
    res = client.post(f"{API}/products/1/reviews", json={"rating": 5}, headers=customer_headers)
    assert res.status_code == 403


def test_review_berhasil_dan_rata_rata(client, customer_headers, admin_headers):
    beli_sampai_diterima(client, customer_headers, admin_headers)
    res = client.post(f"{API}/products/1/reviews", json={"rating": 4, "comment": "Bagus"}, headers=customer_headers)
    assert res.status_code == 201
    assert res.json()["user_name"] == "Budi"

    produk = client.get(f"{API}/products/1").json()
    assert produk["avg_rating"] == 4
    assert produk["review_count"] == 1


def test_review_dua_kali_ditolak(client, customer_headers, admin_headers):
    beli_sampai_diterima(client, customer_headers, admin_headers)
    client.post(f"{API}/products/1/reviews", json={"rating": 5}, headers=customer_headers)
    res = client.post(f"{API}/products/1/reviews", json={"rating": 1}, headers=customer_headers)
    assert res.status_code == 409


def test_rating_harus_1_sampai_5(client, customer_headers):
    res = client.post(f"{API}/products/1/reviews", json={"rating": 6}, headers=customer_headers)
    assert res.status_code == 422


def test_admin_tidak_bisa_review(client, admin_headers):
    res = client.post(f"{API}/products/1/reviews", json={"rating": 5}, headers=admin_headers)
    assert res.status_code == 403
