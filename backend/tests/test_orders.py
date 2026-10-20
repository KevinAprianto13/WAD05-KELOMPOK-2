from tests.conftest import register

API = "/api/v1"
ALAMAT = {"shipping_address": "Jl. Merdeka No. 10, Jakarta"}


def stok_produk(client):
    return client.get(f"{API}/products/1").json()["stock"]


def test_jumlah_negatif_ditolak(client, customer_headers):
    res = client.post(f"{API}/cart/items", json={"product_id": 1, "quantity": -5}, headers=customer_headers)
    assert res.status_code == 422


def test_stok_tidak_cukup(client, customer_headers):
    res = client.post(f"{API}/cart/items", json={"product_id": 1, "quantity": 11}, headers=customer_headers)
    assert res.status_code == 400


def test_checkout_mengurangi_stok(client, customer_headers):
    client.post(f"{API}/cart/items", json={"product_id": 1, "quantity": 3}, headers=customer_headers)
    res = client.post(f"{API}/orders/checkout", json=ALAMAT, headers=customer_headers)
    assert res.status_code == 201
    assert res.json()["total_price"] == 450000
    assert stok_produk(client) == 7
    assert client.get(f"{API}/cart", headers=customer_headers).json()["items"] == []


def test_checkout_keranjang_kosong(client, customer_headers):
    res = client.post(f"{API}/orders/checkout", json=ALAMAT, headers=customer_headers)
    assert res.status_code == 400


def test_alur_status_pesanan(client, customer_headers, admin_headers):
    client.post(f"{API}/cart/items", json={"product_id": 1, "quantity": 1}, headers=customer_headers)
    order_id = client.post(f"{API}/orders/checkout", json=ALAMAT, headers=customer_headers).json()["id"]

    for status in ["processing", "shipped", "delivered"]:
        res = client.put(f"{API}/orders/{order_id}/status", json={"status": status}, headers=admin_headers)
        assert res.status_code == 200

    # Pesanan yang sudah selesai tidak boleh mundur ke pending
    res = client.put(f"{API}/orders/{order_id}/status", json={"status": "pending"}, headers=admin_headers)
    assert res.status_code == 400


def test_batal_mengembalikan_stok(client, customer_headers, admin_headers):
    client.post(f"{API}/cart/items", json={"product_id": 1, "quantity": 4}, headers=customer_headers)
    order_id = client.post(f"{API}/orders/checkout", json=ALAMAT, headers=customer_headers).json()["id"]
    assert stok_produk(client) == 6

    client.put(f"{API}/orders/{order_id}/status", json={"status": "cancelled"}, headers=admin_headers)
    assert stok_produk(client) == 10


def test_customer_hanya_melihat_pesanan_sendiri(client, customer_headers):
    client.post(f"{API}/cart/items", json={"product_id": 1, "quantity": 1}, headers=customer_headers)
    client.post(f"{API}/orders/checkout", json=ALAMAT, headers=customer_headers)

    lain = register(client, "ani@test.com", "ani123456")
    assert client.get(f"{API}/orders/me", headers=lain).json() == []


def test_dashboard_tidak_menghitung_admin(client, customer_headers, admin_headers):
    stats = client.get(f"{API}/admin/dashboard/stats", headers=admin_headers).json()
    assert stats["total_customers"] == 1
