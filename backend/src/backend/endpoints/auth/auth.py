# todo
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
import mariadb
from crypto.jwt import create_access_token
from db.mariadb import db_connection, execute_query
from endpoints.auth.models import SignupRequest, Token
from crypto.password import get_salt, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
def login(
    data: Annotated[OAuth2PasswordRequestForm, Depends()], 
    conn: mariadb.Connection = Depends(db_connection)
) -> Token:
    #Recover password_hash and salt
    query = "SELECT password_hash, salt FROM users WHERE user = ?"
    result = execute_query(conn, query, (data.username,))
    
    if not result:
        raise HTTPException(status_code=401, detail="Email o password errati")

    stored_hash, stored_salt_hex = result[0] 
    stored_salt = bytes.fromhex(stored_salt_hex)

    #Verify password
    if not verify_password(stored_hash, stored_salt, data.password):
        raise HTTPException(status_code=401, detail="Email o password errati")

    return Token(access_token=create_access_token({"sub": data.username}), token_type="bearer")


@router.post("/signup")
def signup(data: SignupRequest, conn: mariadb.Connection = Depends(db_connection)) -> Token:
    salt_pwd = get_salt(16)
    salt_hex = salt_pwd.hex()

    pwd_hash = hash_password(data.password, salt_pwd)

    # Controlla se utente o email esistono già
    check_query = "SELECT id FROM users WHERE user = ? OR email = ?"
    existing = execute_query(conn, check_query, (data.username, data.email))
    if existing:
        raise HTTPException(status_code=400, detail="Username o email già registrati")
    
    insert_query = """
        INSERT INTO users (user, email, password_hash, salt, date)
        VALUES (?, ?, ?, ?, NOW())
    """
    execute_query(conn, insert_query, (data.username, data.email, pwd_hash, salt_hex), fetch=False)
    
    return Token(access_token=create_access_token({"sub": data.username}), token_type="bearer")
