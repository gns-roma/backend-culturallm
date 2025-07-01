import hashlib
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Response
import mariadb
import pydenticon
from exceptions import Error
from endpoints.profile.models import UpdateUserData
from endpoints.auth.auth import get_current_user
from db.mariadb import db_connection, execute_query


router = APIRouter(prefix="/profile", tags=["profile"])

generator = pydenticon.Generator(
        5, 5,
        digest=hashlib.sha1,
        foreground = [ "rgb(128,36,51)" ],
        background="rgb(255,255,255)",
    )


@router.get("/")
def profile(
    current_user: Annotated[str, Depends(get_current_user)], 
    db: Annotated[mariadb.Connection, Depends(db_connection)]
) -> dict:
    """
    Retrieve the profile of the current user.
    """
    get_query = """
        SELECT username, email, signup_date, last_login
        FROM users 
        WHERE username = ?
    """
    result = execute_query(db, get_query, (current_user,), dict=True, fetchone=True)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result


@router.put("/edit/")
def edit_profile(
    current_user: Annotated[str, Depends(get_current_user)],
    db: Annotated[mariadb.Connection, Depends(db_connection)],
    data : UpdateUserData
) -> Response:
    """
    Edit the profile of the current user.
    """
    if not data.email and not data.password:
        raise HTTPException(status_code=400, detail="No fields to update")

    update_fields = []
    params = []

    if data.email:
        update_fields.append("email = ?")
        params.append(data.email)
    
    if data.password:
        from crypto.password import get_salt, hash_password
        salt_pwd = get_salt(16)
        salt_hex = salt_pwd.hex()
        pwd_hash = hash_password(data.password, salt_pwd)

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



@router.get("/avatar/", response_class=Response, responses={
    200: {
        "content": {
            "image/png": {
                "example": "base64_encoded_image_data"
            }
        },
    },
    401: {
        "model": Error,
        "description": "Unauthorized",
    }
})
def get_avatar(
    current_user: Annotated[str, Depends(get_current_user)]
) -> Response:
    """
    Retrieve the avatar of the current user.
    """
    image = generator.generate(
        data = current_user, 
        width = 200, 
        height = 200, 
        padding = (20, 20, 20, 20),
        output_format='png'
    )

    return Response(content=image, media_type="image/png")