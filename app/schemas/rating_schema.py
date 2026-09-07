from pydantic import BaseModel
from typing import Literal

class RatingRequest(BaseModel):
    message_id: int
    feedback: Literal[1, 0]
    content: str | None = None 

class RatingResponse(BaseModel):
    message_id: int
    status: str
