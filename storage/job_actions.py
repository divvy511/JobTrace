from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class JobAction(BaseModel):
    company_name: str
    role: str
    recruiter_name: Optional[str] = ""
    action_type: str
    channel: str
    confidence: Optional[float] = None
    notes: Optional[str] = ""
    timestamp: datetime = Field(default_factory=datetime.utcnow)
