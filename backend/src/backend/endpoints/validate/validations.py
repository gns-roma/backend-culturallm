from fastapi import APIRouter, Depends, Response
from typing import Literal, Optional
from fastapi.routing import APIRoute
import mariadb
from db.mariadb import db_connection, execute_query
from endpoints.auth.auth import get_current_user

router = APIRouter(prefix="/validation", tags=["validation"])

@router.post("/rating")
def rate_answers(
    rating: int,
    answer_id: int,
    flag_ia: bool, 
    db: mariadb.Connection = Depends(db_connection),
    current_user: Optional[str] = Depends(get_current_user),
    type: Literal["human", "llm"] = "human")->Response:

    if type == "human" and current_user is None:
        return Response(status_code=401, content="Unauthorized: User must be logged in to validate an answer.")
    username = current_user if type == "human" else None
    
    insert_query = """
        INSERT INTO ratings (id_answer, username, rating, flag_ia)
        VALUES (?, ?, ?, ?)
    """
    params = (answer_id, username, rating, flag_ia, )
    execute_query(db, insert_query, params, fetch=False)
    return Response(status_code=201)



