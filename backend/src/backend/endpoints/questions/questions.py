from typing import Annotated, Literal, Optional, List
from fastapi import APIRouter, Depends, HTTPException, Response
import mariadb

from endpoints.questions.models import Question, QuestionValues
from db.mariadb import db_connection, execute_query
from endpoints.auth.auth import get_current_user
from endpoints.answers.models import Answer


router = APIRouter(prefix="/questions", tags=["questions"])


@router.post("/")
def submit_question(
    data: QuestionValues,
    db: Annotated[mariadb.Connection, Depends(db_connection)],
    current_user: Annotated[Optional[str], Depends(get_current_user)] = None,
    type: Literal["human", "llm"] = "human"
) -> Response:
    """
    Submit a question to the system.
    """
    if type == "human" and current_user is None:
        return Response(status_code=401, content="Unauthorized: User must be logged in to submit a human question.")
    
    username = current_user if type == "human" else None
    # TODO: Si potrebbe aggiungere un controllo per evitare domande duplicate, anche se poco probabile
    # che due utenti scrivano la stessa domanda
    # TODO: Nella query dovremo anche inserire la valutazione dell'IA della domanda che deve essere un 
    # integer da 1 a 10, più un commento opzionale sulla domanda
    insert_query = """
        INSERT INTO questions (question, topic, type, username) 
        VALUES (?, ?, ?, ?)
    """
    # TODO: Inserire subito risposta della IA alla domanda
    params = (data.question, data.topic, type, username)

    #Oppure potremmo inserirla, farla validare e in modo asincrono aggiornare la riga
    try:
        execute_query(db, insert_query, params, fetch=False)
    except Exception as e:
        print(f"Errore DB: {e}")
        raise HTTPException(status_code=500, detail="Errore inserimento domanda")
    return Response(status_code=201)


@router.get("/random/to_answer")
def get_random_question_to_answer(
    db: Annotated[mariadb.Connection, Depends(db_connection)],
    current_user: Annotated[Optional[str], Depends(get_current_user)] = None,
    type: Literal["human", "llm"] = "human"
) -> Question:
    """
    Retrieve a random question.
    """    
    if current_user is None and type == "human":
        raise HTTPException(
            status_code=401,
            detail="Unauthorized: User must be logged in to answer a question.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if type == "human":
        username = current_user
    #Ritorna una domanda casuale che non è stata ne scritta ne a cui l'utente ha già risposto
    select_query = """
        SELECT q.id, q.type, q.username, q.question, q.topic, q.cultural_specificity, q.cultural_specificity_notes
        FROM questions q
        WHERE q.username != ? AND q.id NOT IN (SELECT question_id FROM answers WHERE username = ?)
        ORDER BY RAND()
        LIMIT 1
        """
    params = (username, username)
    row = execute_query(db, select_query, params, fetchone=True, dict=True)
    if row is None:
        raise HTTPException(status_code=404, detail="Nessuna domanda disponibile.")
    return Question(**row)

@router.get("/random")
def get_random_question(
    db: Annotated[mariadb.Connection, Depends(db_connection)]
) -> Question:
    """
    Retrieve a random question.
    """    
    #Ritorna una domanda casuale con almeno una risposta
    select_query = """
        SELECT q.id, q.type, q.username, q.question, q.topic, q.cultural_specificity, q.cultural_specificity_notes
        FROM questions q JOIN answers a on q.id = a.question_id
        ORDER BY RAND()
        LIMIT 1
        """
    row = execute_query(db, select_query, fetchone=True, dict=True)
    if row is None:
        raise HTTPException(status_code=404, detail="Nessuna domanda disponibile.")
    return Question(**row)



@router.get("/{question_id}")
def get_question(question_id: int, db: Annotated[mariadb.Connection, Depends(db_connection)])->Question:
    """
    Retrieve a question by its ID.
    """
    select_query = """
        SELECT id, type, username, question, topic, cultural_specificity, cultural_specificity_notes 
        FROM questions 
        WHERE id = ?
    """
    params = (question_id,)
    row = execute_query(db, select_query, params,fetchone=True, dict=True)
    if not row:
        raise HTTPException(status_code=404, detail="Nessuna domanda trovata")
    return Question(**row)



@router.get("/{question_id}/answers")
def get_answers_to_question(question_id: int, 
    db: Annotated[mariadb.Connection, Depends(db_connection)],
    current_user: Annotated[Optional[str], Depends(get_current_user)] = None,
    type: Literal["human", "llm"] = "human")-> List[Answer]:

    if type == "human" and current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized: User must be logged in to answer a question.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    username = current_user if type == "human" else None

    """
    Retrieve answers to a question by its ID
    """
    """
    Noi qua prendiamo una risposta casuale a una domanda, affinche il current_user la possa validare, 
    quindi dobbiamo escludere le risposte che l'utente ha scritto oppure che ha già valutato 
    """
    select_query = """
        SELECT id, type, username, question_id, answer
        FROM answers
        WHERE question_id = ?
        EXCEPT
        SELECT a.id, a.type, a.username, a.question_id, a.answer
        FROM answers a LEFT JOIN ratings r ON a.id = r.answer_id
        WHERE a.question_id = ? AND (a.username = ? OR r.username = ?)
    """
    params = (question_id, question_id, username, username)
    rows = execute_query(db, select_query, params, dict=True)
    if not rows:
        raise HTTPException(status_code=404, detail="No answers found for the question")
    #Noi qua prendiamo tutte le risposte a una certa domanda,
    # affinche l'utente le possa poi validare, quindi dobbiamo 
    # filtrare le risposte che l'utente ha scritto lui o che ha già valutato
    #Il modello LLM invece dovrebbe valutare subito una risposta, appena un utente fa il submit
    return [Answer(**row) for row in rows]




@router.get("/{question_id}/answer")
def get_single_answer_to_question(
    question_id: int,
    db: Annotated[mariadb.Connection, Depends(db_connection)],
    current_user: Annotated[Optional[str], Depends(get_current_user)] = None,
    type: Literal["human", "llm"] = "human",
) -> Answer:
    """
    Restituisce UNA risposta alla domanda `question_id` che l'utente
    corrente non ha creato né già valutato.
    Preferisce la risposta con il minor numero di rating.
    """

    if type == "human" and current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized: User must be logged in for this operation.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    username = current_user


    select_query = """
        SELECT
            a.id,
            a.type,
            a.username,
            a.question_id,
            a.answer,
            COUNT(r_count.id) AS rating_count
        FROM
            answers a
        LEFT JOIN
            ratings r_user ON a.id = r_user.answer_id AND r_user.username = ?
        LEFT JOIN
            ratings r_count ON a.id = r_count.answer_id
        WHERE
            a.question_id = ?
            AND (a.username IS NULL OR a.username <> ?)
            AND r_user.id IS NULL
        GROUP BY
            a.id, a.type, a.username, a.question_id, a.answer
        ORDER BY
            rating_count ASC, RAND()
        LIMIT 1
    """


    params = (username, question_id, username)

    row = execute_query(db, select_query, params, fetchone=True, dict=True)

    if not row:
        raise HTTPException(status_code=404, detail="No suitable answer found for the given criteria.")

    return Answer(**row)

