import jwt
from datetime import datetime, timedelta

SECRET_KEY = "ade80556c6e8ce1fa9c1b15a46e1c345d7423fde8c6c0c471a90d54cbe9eee5a"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

#encode data in a token
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

#decode token and return a dict with data
def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token scaduto")
    except jwt.InvalidTokenError:
        raise ValueError("Token non valido")