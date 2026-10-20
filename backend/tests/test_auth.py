from tests.conftest import register

API = "/api/v1"


def test_register_berhasil(client):
    res = client.post(f"{API}/auth/register",
                      json={"email": "siti@test.com", "full_name": "Siti", "password": "siti12345"})
    assert res.status_code == 201
    assert res.json()["user"]["role"] == "customer"
    assert "hashed_password" not in res.json()["user"]


def test_register_password_terlalu_pendek(client):
    res = client.post(f"{API}/auth/register",
                      json={"email": "siti@test.com", "full_name": "Siti", "password": "123"})
    assert res.status_code == 422


def test_login_password_salah(client):
    register(client)
    res = client.post(f"{API}/auth/login", json={"email": "budi@test.com", "password": "salah12345"})
    assert res.status_code == 401


def test_login_dibatasi_rate_limit(client):
    for _ in range(5):
        client.post(f"{API}/auth/login", json={"email": "x@test.com", "password": "salah12345"})
    res = client.post(f"{API}/auth/login", json={"email": "x@test.com", "password": "salah12345"})
    assert res.status_code == 429


def test_endpoint_butuh_token(client):
    assert client.get(f"{API}/cart").status_code == 401


def test_customer_tidak_bisa_akses_admin(client, customer_headers):
    assert client.get(f"{API}/admin/dashboard/stats", headers=customer_headers).status_code == 403
    assert client.post(f"{API}/products", json={"name": "X", "price": 1000},
                       headers=customer_headers).status_code == 403
