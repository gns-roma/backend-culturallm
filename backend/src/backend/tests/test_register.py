from fastapi.testclient import TestClient
from backend import app

client = TestClient(app)
access_token = None

def test_signup():
    response = client.post("/auth/signup/", json={"username": "sorcarlo", "email": "carlo.verdone1927@gmail.com", "password": "forzamaggica1927"})
    assert response.status_code == 422
    response = client.post("/auth/signup/", json={"username": "sorcarlo", "email": "carlo.verdone1927@gmail.com", "password": "forzamaggica1927!"})
    assert response.status_code == 200
    response = client.post("/auth/signup/", json={"username": "Mariano", "email": "marianogiusti@libero.it", "password": "luit1perdon4!"})
    assert response.status_code == 200
    response = client.post("/auth/signup/", json={"username": "Mariano", "email": "marianogiusti@libero.it", "password": "luit1perdon4!"})
    assert response.status_code == 400
    response = client.post("/auth/signup/", json={"username": "hahah", "email": "noemail", "password": "prova"})
    assert response.status_code == 422
    response = client.post("/auth/signup/", json={"username": "hahah", "email": "noemail@silos", "password": "prova"})
    assert response.status_code == 422
    
def test_login():
    response = client.post("/auth/login/", data={"username": "sorcarlo", "password": "forzamaggica1927!"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    global access_token
    access_token = response.json()["access_token"]

def test_profile():
    headers = {"Authorization": f"Bearer {access_token}"}
    print(headers)
    response = client.get("/profile/", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"username": "sorcarlo", "email": "carlo.verdone1927@gmail.com", "date": response.json()["date"]}