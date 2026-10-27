import app as app_module

def test_health_endpoint():
    client = app_module.app.test_client()
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"

def test_empty_analysis_is_rejected():
    client = app_module.app.test_client()
    response = client.post("/api/analyze", json={"text": "  "})
    assert response.status_code == 400
