from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Response
import mariadb
from endpoints.auth.auth import get_current_user
from db.mariadb import db_connection, execute_query


router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("/")
def profile(
    current_user: Annotated[str, Depends(get_current_user)], 
    db: Annotated[mariadb.Connection, Depends(db_connection)]
) -> dict:
    """
    Retrieve the profile of the current user.
    """
    get_query = """
        SELECT username, email, signup_date 
        FROM users 
        WHERE username = ?
    """
    result = execute_query(db, get_query, (current_user,))
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = result[0]
    return {"username": user_data[0], "email": user_data[1], "date": user_data[2]}


@router.put("/edit")
def edit_profile(
    current_user: Annotated[str, Depends(get_current_user)],
    db: Annotated[mariadb.Connection, Depends(db_connection)],
    email: str | None = None,
    password: str | None = None
) -> Response:
    """
    Edit the profile of the current user.
    """
    if not email and not password:
        raise HTTPException(status_code=400, detail="No fields to update")

    update_fields = []
    params = []

    if email:
        update_fields.append("email = ?")
        params.append(email)
    
    if password:
        from crypto.password import get_salt, hash_password
        salt_pwd = get_salt(16)
        salt_hex = salt_pwd.hex()
        pwd_hash = hash_password(password, salt_pwd)

        update_fields.append("password_hash = ?, salt = ?")
        params.extend([pwd_hash, salt_hex])

    params.append(current_user)
    
    update_query = f"""
        UPDATE users 
        SET {', '.join(update_fields)}
        WHERE user = ?
        """
    
    execute_query(db, update_query, tuple(params), fetch=False)
    
    return Response(status_code=204)  # No Content, successful update without returning data