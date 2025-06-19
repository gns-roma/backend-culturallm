from fastapi.testclient import TestClient
import pytest

from backend import app

#RISCRIVERLI TUTTI MEGLIO
client = TestClient(app)


@pytest.mark.order(4)
def test_login():
    global access_token1, access_token2

    response = client.post("/auth/login/", data={"username": "sorcarlo", "password": "forzamaggica1927!"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    access_token1 = response.json()["access_token"]

    response = client.post("/auth/login/", data={"username": "Mariano", "email": "marianogiusti@libero.it", "password": "luit1perdon4!"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    access_token2 = response.json()["access_token"]


@pytest.mark.order(5)
def test_submit_question():
    headers1 = {"Authorization": f"Bearer {access_token1}"}
    headers2 = {"Authorization": f"Bearer {access_token2}"}

    response = client.post("/questions/", params={"question": "Chi ha incontrato Gesù sulla A24?", "topic": "arte", "type": "human"}, headers=headers1)
    assert response.status_code == 201

    response = client.post("/questions/", params={"question": "Quando arriva il papa nero?", "topic": "arte", "type": "human"})
    assert response.status_code == 401

    response = client.post("/questions/", params={"question": "Chi ha interpretato il ruolo di Padre Frediani?", "topic": "arte", "type": "human"}, headers=headers2)
    assert response.status_code == 201

@pytest.mark.order(6)
def test_get_answer_and_validate():
    headers1 = {"Authorization": f"Bearer {access_token1}"}
    headers2 = {"Authorization": f"Bearer {access_token2}"}

    question_id_1: int | None = None
    question_id_2: int | None = None

    random_response = client.get("/questions/random", headers=headers1)
    if random_response.status_code == 200:
        question_id_1 = random_response.json()["id"]

        print("Random question retrieved successfully: ", question_id_1,random_response.json()["question"])
        answer_response = client.post("/answers/", params={
            "answer": "Il compianto Fabrizio Frizzi ha interpretato il ruolo di Padre Frediani.",
            "question_id": question_id_1,
            "type": "human"
        }, headers=headers1)
        assert answer_response.status_code == 201


    random_response = client.get("/questions/random", headers=headers2)
    if random_response.status_code == 200:
        question_id_2= random_response.json()["id"]

        print("Random question retrieved successfully: ", question_id_2,random_response.json()["question"])
        answer_response = client.post("/answers/", params={
            "answer": "Il grande Mariano Giusti ha incontrato Gesù sulla A24.",
            "question_id": question_id_2,
            "type": "human"
        }, headers=headers2)
        assert answer_response.status_code == 201

    answers_response = client.get(f"/questions/{question_id_1}/answers")
    assert answers_response.status_code in (200, 404)

    answer_id_1: int | None = None
    answer_id_2: int | None = None

    if answers_response.status_code == 200:
        answers = answers_response.json()
        answer_id_1 = answers[0]["id"]
        assert isinstance(answers, list)
        print("Answers for question 1:", answers)
    
    rating_response = client.post("/validation/rating", params={
        "rating": 5,
        "answer_id": answer_id_1,
        "flag_ia": False
    }, headers=headers2)
    assert rating_response.status_code == 201
    
    answers_response = client.get(f"/questions/{question_id_2}/answers")
    assert answers_response.status_code in (200, 404)
    if answers_response.status_code == 200:
        answers = answers_response.json()
        answer_id_2 = answers[0]["id"]
        assert isinstance(answers, list)
        print("Answers for question 2:", answers)

    rating_response = client.post("/validation/rating", params={
        "rating": 5,
        "answer_id": answer_id_2,
        "flag_ia": False
    }, headers=headers1)
    assert rating_response.status_code == 201

    validations_response = client.get(f"/answers/{answer_id_1}/validations")
    assert validations_response.status_code == 200

    if validations_response.status_code == 200:
        validations = validations_response.json()
        assert isinstance(validations, list)
        print("Validations for answer 1:", validations)

    validations_response = client.get(f"/answers/{answer_id_2}/validations")
    assert validations_response.status_code == 200

    if validations_response.status_code == 200:
        validations = validations_response.json()
        assert isinstance(validations, list)
        print("Validations for answer 2:", validations)