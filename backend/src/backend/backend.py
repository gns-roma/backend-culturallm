import logging
from fastapi import FastAPI
from endpoints.questions import topics, questions
from endpoints.profile import profile
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
app.include_router(topics.router)
app.include_router(questions.router)