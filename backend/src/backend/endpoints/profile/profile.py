from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
import mariadb
from db.mariadb import db_connection, execute_query


from endpoints.profile.models import User
from crypto.jwt import decode_access_token


router = APIRouter(prefix="/profile", tags=["profile"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token : Annotated[str, Depends(oauth2_scheme)]) -> str:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    return username

@router.get("/me")
def profile(
    current_user: Annotated[str, Depends(get_current_user)], 
    db: Annotated[mariadb.Connection, Depends(db_connection)]
) -> dict:
    """
    Retrieve the profile of the current user.
    """
    get_query = "SELECT user, email, date FROM users WHERE user = ?"
    result = execute_query(db, get_query, (current_user,))
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = result[0]
    return {"username": user_data[0], "email": user_data[1], "date": user_data[2]}
