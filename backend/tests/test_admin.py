import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.config import settings

client = TestClient(app)

@pytest.fixture
def admin_token():
    res = client.post("/api/auth/login", json={
        "email": settings.ADMIN_EMAIL,
        "password": settings.ADMIN_PASSWORD
    })
    assert res.status_code == 200
    return res.json()["access_token"]

def test_admin_routes_unauthenticated():
    endpoints = [
        "/api/admin/system-info",
        "/api/admin/reports",
        "/api/admin/entities",
        "/api/admin/export/1930",
        "/api/admin/audit-log"
    ]
    for ep in endpoints:
        res = client.get(ep)
        assert res.status_code == 401, f"Expected 401 for unauthenticated {ep}, got {res.status_code}"

def test_admin_system_info(admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    res = client.get("/api/admin/system-info", headers=headers)
    assert res.status_code == 200
    assert "no-store" in res.headers.get("Cache-Control", "")

    data = res.json()
    assert data["status"] == "healthy"
    assert "models" in data
    assert "database_counts" in data
    assert "live_user" in data["database_counts"]
    assert "demo_seed" in data["database_counts"]
    assert "test_traffic" in data["database_counts"]

def test_admin_reports_moderation(admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    res = client.get("/api/admin/reports?status_filter=ALL", headers=headers)
    assert res.status_code == 200
    reports = res.json()
    assert isinstance(reports, list)

    if reports:
        rep_id = reports[0]["id"]
        # Update status
        update_res = client.post(f"/api/admin/reports/{rep_id}/status?status=RESOLVED", headers=headers)
        assert update_res.status_code == 200
        assert update_res.json()["new_status"] == "RESOLVED"

def test_admin_community_entities(admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    # List entities
    res = client.get("/api/admin/entities", headers=headers)
    assert res.status_code == 200
    entities = res.json()
    assert isinstance(entities, list)

    # Add entity
    add_res = client.post(
        "/api/admin/entities?entity_type=vpa&entity_value=scammer-test@okhdfcbank&scam_category=phishing_kyc",
        headers=headers
    )
    assert add_res.status_code == 200
    new_id = add_res.json()["id"]

    # Delete entity
    del_res = client.delete(f"/api/admin/entities/{new_id}", headers=headers)
    assert del_res.status_code == 200

def test_admin_1930_export(admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    # Test JSON export
    res_json = client.get("/api/admin/export/1930?export_format=json", headers=headers)
    assert res_json.status_code == 200
    data = res_json.json()
    assert "disclaimer" in data
    assert "1930" in data["disclaimer"] or "law enforcement" in data["disclaimer"]
    assert "incidents" in data

    # Test CSV export
    res_csv = client.get("/api/admin/export/1930?export_format=csv", headers=headers)
    assert res_csv.status_code == 200
    assert "text/csv" in res_csv.headers.get("content-type", "")
    assert "LEGAL DISCLAIMER" in res_csv.text or "DISCLAIMER" in res_csv.text

def test_admin_audit_log(admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    res = client.get("/api/admin/audit-log?limit=10&data_source=all", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert "total" in data
    assert "items" in data
    assert isinstance(data["items"], list)
