from fastapi import APIRouter


router = APIRouter(tags=["questions"])


@router.get("/topics")
def get_topics():
    """
    Retrieve a list of available topics.
    """
    topics = [
        "cibo",
        "sport",
        "cinema",
        "musica",
    ]
    return {"topics": topics}