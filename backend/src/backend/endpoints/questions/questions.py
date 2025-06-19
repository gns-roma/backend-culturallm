from typing import Annotated, Literal, Optional, List
from fastapi import APIRouter, Depends, HTTPException, Response
import mariadb

from endpoints.questions.models import Question
from db.mariadb import db_connection, execute_query
from endpoints.auth.auth import get_current_user
from endpoints.answers.models import Answer


router = APIRouter(prefix="/questions", tags=["questions"])


@router.post("/")
def submit_question(
    question: str, 
    topic: str,
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
    # TODO: Si potrebbe aggiungere un controllo per evitare domande duplicate
    # TODO: Nella query dovremo anche inserire la valutazione dell'IA della domanda
    insert_query = """
        INSERT INTO questions (question, topic, type, username) 
        VALUES (?, ?, ?, ?)
    """
    params = (question, topic, type, username)

    #Oppure potremmo inserirla, farla validare e in modo asincrono aggiornare la riga
    try:
        execute_query(db, insert_query, params, fetch=False)
    except Exception as e:
        print(f"Errore DB: {e}")
        raise HTTPException(status_code=500, detail="Errore inserimento domanda")
    return Response(status_code=201)


@router.get("/random")
def get_random_question(
    db: Annotated[mariadb.Connection, Depends(db_connection)],
    current_user: Annotated[Optional[str], Depends(get_current_user)] = None,
    type: Literal["human", "llm"] = "human"
) -> Question:
    #MODIFICA DA VALUTARE
    if type == "human" and current_user is None:
        return Response(status_code=401, content="Unauthorized: User must be logged in to answer a question.")
    
    username = current_user if type == "human" else None
    """
    Retrieve a random question.
    """    
    select_query = """
        SELECT id, type, username, question, topic, cultural_specificity, cultural_specificity_notes 
        FROM questions 
        WHERE username != ?
        ORDER BY RAND()
        LIMIT 1
    """
    params = (username, )
    row = execute_query(db, select_query, params, fetchone=True, dict=True)
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
def get_answers_to_question(question_id: int, db: Annotated[mariadb.Connection, Depends(db_connection)])->List[Answer]:
    """
    Retrieve answers to a question by its ID
    """
    select_query = """
        SELECT id, type, username, question_id, answer
        FROM answers
        WHERE question_id = ?
    """
    params = (question_id, )
    rows = execute_query(db, select_query, params,dict=True)
    if not rows:
        raise HTTPException(status_code=404, detail="No answers found for the question")
    return [Answer(**row) for row in rows]