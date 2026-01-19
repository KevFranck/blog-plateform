from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_and_get_article():
    payload = {"title": "Hello World", "content": "My first post", "status": "draft"}
    r = client.post("/articles", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["title"] == "Hello World"
    assert data["content"] == "My first post"
    assert data["status"] == "draft"
    assert data["id"]

    article_id = data["id"]
    r2 = client.get(f"/articles/{article_id}")
    assert r2.status_code == 200
    data2 = r2.json()
    assert data2["id"] == article_id


def test_unique_title():
    payload = {"title": "Unique Title", "content": "A", "status": "draft"}
    r1 = client.post("/articles", json=payload)
    assert r1.status_code == 201

    r2 = client.post("/articles", json=payload)
    assert r2.status_code == 409
