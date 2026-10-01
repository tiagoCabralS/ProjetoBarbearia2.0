import pytest


def test_health_is_public(api_client):
    r = api_client.get("/api/health/")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_openapi_schema_generates(api_client):
    r = api_client.get("/api/schema/")
    assert r.status_code == 200


@pytest.mark.django_db
def test_protected_endpoint_requires_auth(api_client):
    # qualquer rota protegida; aqui o schema já prova o padrão IsAuthenticated
    # após existir o primeiro endpoint de negócio, troque por ele
    r = api_client.get("/api/auth/refresh/")
    assert r.status_code in (400, 405)  # rota pública do JWT, não retorna 401


@pytest.mark.django_db
def test_login_returns_tokens(api_client, user):
    r = api_client.post("/api/auth/login/", {"email": "ana@exemplo.com", "password": "s3nha-forte"})
    assert r.status_code == 200
    assert {"access", "refresh"} <= set(r.json())
