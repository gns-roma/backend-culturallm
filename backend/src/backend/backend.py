import logging
from fastapi import FastAPI, HTTPException
from pydantic import ValidationError


app = FastAPI()

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.INFO)

# se vogliamo attivare i log di debug possiamo settare il livello a logging.DEBUG
# logger.setLevel(logging.DEBUG)