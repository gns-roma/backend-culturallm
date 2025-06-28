from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    username: str
    email: EmailStr
    date: datetime
    #profile_picture: str | None = None

class UpdateUserData(BaseModel):
    email: EmailStr | None = None
    password: str | None = None