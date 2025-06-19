from pydantic import BaseModel, Field


class Rating(BaseModel):
    id: int
    answer_id: int
    username: str | None
    rating: int = Field(..., ge=1, le=5)
    flag_ia: bool