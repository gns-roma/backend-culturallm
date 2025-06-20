import logging
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager

from db.pool import init_pool
from endpoints.questions import topics, questions
from endpoints.profile import profile
from endpoints.auth import auth
from endpoints.answers import answers
from endpoints.validate import validations
from endpoints.gamification import leaderboard


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_pool()
    yield


app = FastAPI(lifespan=lifespan)

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
app.include_router(answers.router)
app.include_router(validations.router)
app.include_router(leaderboard.router)