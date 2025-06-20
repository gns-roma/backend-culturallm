from fastapi.testclient import TestClient
from backend import app

import pytest
from db.pool import init_pool

client = TestClient(app)
access_token = None

@pytest.fixture(scope="session", autouse=True)
def initialize_db_pool():
    init_pool()

@pytest.mark.order(1)
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
    response = client.post("/auth/signup/", json={"username": "tamburini", "email": "tamburini.direttore@gmail.com", "password": "forzamaggica1927!"})
    assert response.status_code == 200
    response = client.post("/auth/signup/", json={"username": "magatrump", "email": "thedonald@gmail.com", "password": "forzamaggica1927!"})
    assert response.status_code == 200
    response = client.post("/auth/signup/", json={"username": "salvobuzzi", "email": "buzzi.salvatore@gmail.com", "password": "forzamaggica1927!"})
    assert response.status_code == 200
    response = client.post("/auth/signup/", json={"username": "cruciani", "email": "cruciani@gmail.com", "password": "forzamaggica1927!"})
    assert response.status_code == 200
    response = client.post("/auth/signup/", json={"username": "tony777", "email": "tonyeffe@gmail.com", "password": "forzamaggica1927!"})
    assert response.status_code == 200
    response = client.post("/auth/signup/", json={"username": "sidebaby", "email": "darkside@gmail.com", "password": "forzamaggica1927!"})
    assert response.status_code == 200
    response = client.post("/auth/signup/", json={"username": "wanna", "email": "wannamarchi@gmail.com", "password": "forzamaggica1927!"})
    assert response.status_code == 200
    response = client.post("/auth/signup/", json={"username": "montalbano", "email": "mantalbano@gmail.com", "password": "forzamaggica1927!"})
    assert response.status_code == 200


    
@pytest.mark.order(2)
def test_login():
    response = client.post("/auth/login/", data={"username": "sorcarlo", "password": "forzamaggica1927!"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    global access_token
    access_token = response.json()["access_token"]

@pytest.mark.order(3)
def test_profile():
    headers = {"Authorization": f"Bearer {access_token}"}
    print(headers)
    response = client.get("/profile/", headers=headers)
    assert response.status_code == 200
    assert response.json() == {
        "username": "sorcarlo", 
        "email": "carlo.verdone1927@gmail.com", 
        "signup_date": response.json()["signup_date"], 
        "last_login": response.json()["last_login"]
    }
