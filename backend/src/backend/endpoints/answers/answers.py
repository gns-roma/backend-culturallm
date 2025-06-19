from fastapi import APIRouter, Depends, Response, HTTPException
from typing import Annotated, Literal, Optional, List
from fastapi.routing import APIRoute
import mariadb
from db.mariadb import db_connection, execute_query
from endpoints.auth.auth import get_current_user
from endpoints.validate.models import Rating


router = APIRouter(prefix="/answers", tags=["answers"])

@router.post("/")
def submit_answer(
    answer: str,
    question_id: int,
    db: Annotated[mariadb.Connection, Depends(db_connection)],
    current_user: Annotated[Optional[str], Depends(get_current_user)] = None,
    type: Literal["human", "llm"] = "human"
) -> Response:
    """
    Submit an answer to a question.
    """
    if type == "human" and current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized: User must be logged in to answer a question.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    username = current_user if type == "human" else None

    # Controllo domanda esistente
    question_query = """
        SELECT id
        FROM questions 
        WHERE id = ?
    """
    question_check = execute_query(db, question_query, (question_id,), fetchone=True)
    print(question_check, flush=True)
    print(f"Question check for id={question_id}: {question_check}")
    if not question_check:
        raise HTTPException(status_code=404, detail="Domanda non trovata")

    insert_query = """
        INSERT INTO answers (question_id, username, type, answer, timestamp) 
        VALUES (?, ?, ?, ?, NOW())
    """
    params = (question_id, username, type, answer)

    try:
        execute_query(db, insert_query, params, fetch=False)
    except Exception as e:
        print(f"Errore durante l'inserimento risposta: {e}")
        raise HTTPException(status_code=500, detail="Errore interno durante l'inserimento della risposta")
    return Response(status_code=201)

@router.get("/{answer_id}/validations")
def get_validations_to_answer(answer_id: int, db: Annotated[mariadb.Connection, Depends(db_connection)])->List[Rating]:
    """
    Retrieve ratings by its answer_ID.
    """
    select_query = """
        SELECT id, answer_id,question_id, username, rating, flag_ia 
        FROM ratings
        WHERE answer_id = ?
    """
    params = (answer_id,)
    rows = execute_query(db, select_query, params, dict=True)
    if not rows:
        raise HTTPException(status_code=404, detail="No answers found for the question")
    return [Rating(**row) for row in rows]