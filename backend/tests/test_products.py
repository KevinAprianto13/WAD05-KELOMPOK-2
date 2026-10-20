from tests.conftest import register

API = "/api/v1"


def test_daftar_produk(client):
    res = client.get(f"{API}/products")
    assert res.status_code == 200
    assert len(res.json()) == 1


def test_cari_produk(client):
    assert len(client.get(f"{API}/products", params={"search": "mouse"}).json()) == 1
    assert len(client.get(f"{API}/products", params={"search": "kulkas"}).json()) == 0


def test_limit_dibatasi(client):
    assert client.get(f"{API}/products", params={"limit": 100000}).status_code == 422


def test_harga_negatif_ditolak(client, admin_headers):
    res = client.post(f"{API}/products", json={"name": "Keyboard", "price": -1000}, headers=admin_headers)
    assert res.status_code == 422


def test_produk_nonaktif_tidak_bisa_dibuka(client, admin_headers):
    client.delete(f"{API}/products/1", headers=admin_headers)
    assert client.get(f"{API}/products/1").status_code == 404


def test_kategori_dipakai_tidak_bisa_dihapus(client, admin_headers):
    assert client.delete(f"{API}/categories/1", headers=admin_headers).status_code == 400


def test_chat_customer_selalu_ke_admin(client, customer_headers):
    lain = register(client, "ani@test.com", "ani123456")
    ani_id = client.get(f"{API}/auth/me", headers=lain).json()["id"]

    res = client.post(f"{API}/chat/", json={"receiver_id": ani_id, "content": "Halo"}, headers=customer_headers)
    assert res.status_code == 200
    assert res.json()["receiver_id"] != ani_id
