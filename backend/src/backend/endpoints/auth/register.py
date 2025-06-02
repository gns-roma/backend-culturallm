# todo
import mariadb
from db.mariadb import db_connection, execute_query
from endpoints.auth.models import RegisterRequest, Response
from crypto.password import get_salt, hash_password
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError
from datetime import datetime


router = APIRouter()

@router.post("/register")
def register(request: RegisterRequest, conn: mariadb.Connection = Depends(db_connection))->Response:
    salt_pwd = get_salt(16)
    salt_hex = salt_pwd.hex()
    pwd_hash = hash_password(request.password, salt_pwd)
    # Controlla se utente o email esistono già
    check_query = "SELECT id FROM users WHERE user = ? OR email = ?"
    existing = execute_query(conn, check_query, (request.user, request.email))
    if existing:
        raise HTTPException(status_code=400, detail="Username o email già registrati")
    insert_query = """
    INSERT INTO users (user, email, password_hash, salt, date)
    VALUES (?, ?, ?, ?, NOW())
    """
    execute_query(conn, insert_query, (request.user, request.email, pwd_hash, salt_hex), fetch=False)
    
    return Response(status=200)

