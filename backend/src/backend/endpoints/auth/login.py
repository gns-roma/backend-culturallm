# todo
from fastapi import APIRouter, Depends, HTTPException
import mariadb
from db.mariadb import db_connection, execute_query
from endpoints.auth.models import LoginRequest, Response
from crypto.password import verify_password
from typing import Tuple

router = APIRouter()

@router.post("/login")
def login(request: LoginRequest, conn: mariadb.Connection = Depends(db_connection)):
    #Recover password_hash and salt
    query = "SELECT password_hash, salt FROM users WHERE user = ?"
    result = execute_query(conn, query, (request.user,))
    
    if not result:
        raise HTTPException(status_code=401, detail="Email o password errati")

    stored_hash, stored_salt_hex = result[0] 
    stored_salt = bytes.fromhex(stored_salt_hex)

    #Verify password
    if not verify_password(stored_hash, stored_salt, request.password):
        raise HTTPException(status_code=401, detail="Email o password errati")

    return Response(status=True)