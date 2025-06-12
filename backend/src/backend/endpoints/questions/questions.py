from fastapi import APIRouter


router = APIRouter(prefix="/questions", tags=["questions"])

@router.post("/")
def submit_question(question: str):
    """
    Submit a question to the system.
    """
    pass


@router.get("/random")
def get_random_question():
    """
    Retrieve a random question.
    """
    pass


@router.get("/{question_id}")
def get_question(question_id: int):
    """
    Retrieve a question by its ID.
    """
    pass