from unittest.mock import Base
from pydantic import BaseModel, EmailStr, Field, model_validator

class SignupRequest(BaseModel):
    username: str = Field(..., min_length=1)
    email: EmailStr
    password: str = Field(
        ...,
        min_length=12,
        max_length=100,
        pattern=r'^[A-Za-z0-9!@#$%&+=*\-?]+$',
        description="Password must contain only letters, numbers, and allowed symbols: !@#$%&+=*-?"
    )

    @model_validator(mode="after")
    def validate_password_strength(self):
        pwd = self.password
        if not any(c.isdigit() for c in pwd):
            raise ValueError("Password must contain at least one number")
        if not any(c.isalpha() for c in pwd):
            raise ValueError("Password must contain at least one letter")
        # Qui controlliamo simboli coerenti con la regex
        allowed_symbols = set("!@#$%&+=*-?")
        if not any(c in allowed_symbols for c in pwd):
            raise ValueError(f"Password must contain at least one symbol from {''.join(allowed_symbols)}")
        return self
    

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"