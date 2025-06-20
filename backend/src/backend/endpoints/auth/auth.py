from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import InvalidTokenError
import mariadb
from crypto.jwt import create_access_token, decode_access_token
from db.mariadb import db_connection, execute_query
from endpoints.auth.models import SignupRequest, Token
from crypto.password import get_salt, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])

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

@router.post("/login")
def login(
    data: Annotated[OAuth2PasswordRequestForm, Depends()], 
    conn: mariadb.Connection = Depends(db_connection)
) -> Token:
    #Recover password_hash and salt
    auth_query = "SELECT password_hash, salt FROM users WHERE username = ?"
    result = execute_query(conn, auth_query, (data.username,))
    
    if not result:
        raise HTTPException(status_code=401, detail="Email o password errati")

    stored_hash, stored_salt_hex = result[0] 
    stored_salt = bytes.fromhex(stored_salt_hex)

    #Verify password
    if not verify_password(stored_hash, stored_salt, data.password):
        raise HTTPException(status_code=401, detail="Email o password errati")
    
    #Aggiorna last_login
    update_query = """
        UPDATE users 
        SET last_login = NOW()
        WHERE username = ?
    """
    execute_query(conn, update_query, (data.username,), fetch=False)

    return Token(access_token=create_access_token({"sub": data.username}), token_type="bearer")


@router.post("/signup")
def signup(data: SignupRequest, conn: Annotated[mariadb.Connection, Depends(db_connection)]) -> Token:
    salt_pwd = get_salt(16)
    salt_hex = salt_pwd.hex()

    pwd_hash = hash_password(data.password, salt_pwd)

    # Controlla se utente o email esistono già
    check_query = """
        SELECT username 
        FROM users 
        WHERE username = ? OR email = ?
    """
    existing = execute_query(conn, check_query, (data.username, data.email))
    if existing:
        raise HTTPException(status_code=400, detail="Username o email già registrati")
    
    insert_query = """
        INSERT INTO users (username, email, password_hash, salt, signup_date, last_login)
        VALUES (?, ?, ?, ?, NOW(), NOW())
    """
    execute_query(conn, insert_query, (data.username, data.email, pwd_hash, salt_hex), fetch=False)

    return Token(access_token=create_access_token({"sub": data.username}), token_type="bearer")
