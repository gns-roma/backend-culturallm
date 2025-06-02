import logging
import mariadb
from fastapi import FastAPI, HTTPException
from pydantic import ValidationError
from endpoints.auth import register, login
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    conn = mariadb.connect(
        host="culturallm-db",
        port=3306,
        user="user",
        password="userpassword",
        database="culturallm_db"
    )
    conn.close()
    yield


app = FastAPI(lifespan=lifespan)

app.title = "Backend CulturaLLM API"
app.description = "API for managing CulturaLLM project."

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.INFO)
# se vogliamo attivare i log di debug possiamo settare il livello a logging.DEBUG
# logger.setLevel(logging.DEBUG)

app.include_router(login.router)
app.include_router(register.router)