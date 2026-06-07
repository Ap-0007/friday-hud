from fastapi.testclient import TestClient
from local_brain import app

client = TestClient(app)

def test_listen_endpoint():
    response = client.post("/listen")
    assert response.status_code == 200
    assert response.json() == {"status": "success", "text": "Ready when you are, boss."}
