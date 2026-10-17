from  pydantic import BaseModel, Field
from typing import Optional

class TextRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=10000)



class TextResponse(BaseModel):
    task: str
    result: str
    model: str
    tokens_used: Optional[int] = None


class HealthResponse(BaseModel):
    status: str
    provider: str
    model: str
