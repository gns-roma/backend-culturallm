from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated, List
import mariadb
from db.mariadb import db_connection, execute_query
from endpoints.auth.auth import get_current_user
from endpoints.gamification.models import User

router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])

@router.get("/best")
def get_best_leaderboard(db: Annotated[mariadb.Connection, Depends(db_connection)])-> List[User]:
    select_query = """
    SELECT username, score FROM leaderboard ORDER BY score DESC LIMIT 10"""
    users = execute_query(db, select_query, dict = True)
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return [User(**user) for user in users]



@router.get("/")
def get_leaderboard(db: Annotated[mariadb.Connection, Depends(db_connection)])->List[User]:
    select_query = """SELECT username, score FROM leaderboard ORDER BY score"""
    users = execute_query(db, select_query, dict = True)
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return [User(**user) for user in users]



@router.get("/user")
def get_user_position(
    db: Annotated[mariadb.Connection, Depends(db_connection)],
    current_user: Annotated[User, Depends(get_current_user)],
)->User:
    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized: User must be logged in to get their position.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    username = current_user
    select_query = """
    SELECT username, score, (
        SELECT COUNT(*) + 1
        FROM leaderboard
        WHERE score > (SELECT score FROM leaderboard WHERE username = ?)) AS position
    FROM leaderboard
    WHERE username = ?"""
    user = execute_query(db, select_query, (username, username),fetchone=True, dict=True)
    if not user:
        raise HTTPException(status_code=404, detail="No user found")
    return User(**user)
