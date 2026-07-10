# pydantic based request and response schema section 

from typing import Literal
from pydantic import BaseModel, Field 


# items schema 

class ItemsSchema(BaseModel):
    text: str = Field(description="Exact word or short phrase that had the issue")
    start: str = Field(description="Start time in seconds within the audio")
    end: str = Field(description="End time in seconds within the audio")
    issue_type: Literal[
        "mispronunciation",
        "unclear_segment",
        "grammer",
        "word_choice",
        "filler_or_hesitation",
    ]
    explaination: str = Field(description="What specifically went wrong")
    suggestion: str = Field(description="How to say/fix it correctly")



# next class for response we will get 
    
class Response(BaseModel):
    transcript: str 
    duration_seconds: float
    pronunciation_score: int = Field(ge=0, le=100)
    fluency_notes: str
    mistakes: list[ItemsSchema]
    low_confidence_word_count: int 
    audio_object_key: str 
    transcript_object_key: str 
    retention_hours: int 


class ErrorResponse(BaseModel):
    detail: str

    