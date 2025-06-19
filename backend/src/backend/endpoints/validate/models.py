from typing import Literal
from pydantic import BaseModel, model_validator


class Rating(BaseModel):
    id: int
    id_answer: int
    username: str | None
    rating: int
    flag_ia: bool

    @model_validator(mode="after")
    def validate_rating(self):
        if(self.rating > 5 or self.rating<1):
            raise ValueError("Rating must be a value between 1 and 5")
        return self
    
