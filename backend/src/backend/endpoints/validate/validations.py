from fastapi import APIRouter, Depends, HTTPException, Response
from typing import Literal, Optional
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
    type: Literal["human", "llm"] = "human"
) -> Response:

    if type == "human" and current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized: User must be logged in to answer a question.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    username = current_user if type == "human" else None
    
    insert_query = """
        INSERT INTO ratings (answer_id, username, rating, flag_ia)
        VALUES (?, ?, ?, ?)
    """
    params = (answer_id, username, rating, flag_ia)
    execute_query(db, insert_query, params, fetch=False)
    return Response(status_code=201)



