from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class JobAction(BaseModel):
    company: Optional[str]
    role: Optional[str]
    recruiter: Optional[str]
    action: str
    channel: str
    confidence: float
    timestamp: datetime
