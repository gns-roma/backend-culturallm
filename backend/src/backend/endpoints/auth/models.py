from email.policy import HTTP
from pydantic import BaseModel, EmailStr, Field, model_validator

class SignupRequest(BaseModel):
    username: str = Field(..., min_length=1)
    email: EmailStr
    password: str = Field(
        ...,
        min_length=12,
        max_length=100,
        pattern=r'^[A-Za-z0-9!@#$%&+=*\-?]+$', 
        description="La password deve contenere solo lettere, numeri e i simboli ammessi: !@#$%&+=*-?",
        
    )

    @model_validator(mode="after")
    def validate_password(self):
        pwd = self.password
        
        if len(pwd) > 64:
            raise ValueError("La password è troppo lunga")
        if len(pwd) < 8:
            raise ValueError("La password è troppo corta")
        if not any(c.isdigit() for c in pwd):
            raise ValueError("La password deve contenere almeno un numero")
        if not any(c.isalpha() for c in pwd):
            raise ValueError("La password deve contenere almeno una lettera")
        # Qui controlliamo simboli coerenti con la regex
        allowed_symbols = set("!@#$%&+=*-?.")
        if not any(c in allowed_symbols for c in pwd):
            raise ValueError(f"La password deve contenere almeno un simbolo tra {''.join(allowed_symbols)}")
        return self
    

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    refresh_token: str