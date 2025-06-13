from fastapi import APIRouter, Depends, Response
from typing import Literal, Optional
from fastapi.routing import APIRoute
import mariadb

from db.mariadb import db_connection, execute_query
from endpoints.auth.auth import get_current_user


router = APIRouter(prefix="/answers", tags=["answers"])

@router.post("/")
def submit_answer(
    answer: str,
    question_id: int,
    db: mariadb.Connection = Depends(db_connection),
    current_user: Optional[str] = Depends(get_current_user),
    type: Literal["human", "llm"] = "human"
) -> Response:
    """
    Submit an answer to a question.
    """
    if type == "human" and current_user is None:
        return Response(status_code=401, content="Unauthorized: User must be logged in to submit an answer.")
    
    username = current_user if type == "human" else None

    insert_query = """
        INSERT INTO answers (answer, question_id, type, username, timestamp) 
        VALUES (?, ?, ?,, ? NOW())
    """
    params = (answer, question_id, type, username)

    execute_query(db, insert_query, params, fetch=False)
    return Response(status_code=201)
