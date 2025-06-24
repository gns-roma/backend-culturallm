from datetime import datetime
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    username: str
    email: EmailStr
    date: datetime
    #profile_picture: str | None = None