from fastapi.testclient import TestClient
from backend import app

client = TestClient(app)

def test_register():
    response = client.post("/register/", json={"user": "sorcarlo", "email": "carlo.verdone1927@gmail.com", "password": "forzamaggica1927"})
    assert response.status_code == 422
    response = client.post("/register/", json={"user": "sorcarlo", "email": "carlo.verdone1927@gmail.com", "password": "forzamaggica1927!"})
    assert response.status_code == 200
    response = client.post("/register/", json={"user": "Mariano", "email": "marianogiusti@libero.it", "password": "luit1perdon4!"})
    assert response.status_code == 200
    response = client.post("/register/", json={"user": "Mariano", "email": "marianogiusti@libero.it", "password": "luit1perdon4!"})
    assert response.status_code == 400
    response = client.post("/register/", json={"user": "hahah", "email": "noemail", "password": "prova"})
    assert response.status_code == 422