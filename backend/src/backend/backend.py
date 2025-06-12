import logging
from endpoints.profile import profile
from fastapi import FastAPI
from endpoints.auth import auth


app = FastAPI()

app.title = "Backend CulturaLLM API"
app.description = "API for managing CulturaLLM project."

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.INFO)
# se vogliamo attivare i log di debug possiamo settare il livello a logging.DEBUG
# logger.setLevel(logging.DEBUG)

app.include_router(auth.router)
app.include_router(profile.router)