from storage.models import JobAction
from datetime import datetime

def distill_llm_output(data: dict) -> JobAction:
    return JobAction(
        company=data.get("company"),
        role=data.get("role"),
        recruiter=data.get("recruiter"),
        action=data["action"],
        channel=data["channel"],
        confidence=float(data.get("confidence", 0.8)),
        timestamp=datetime.utcnow()
    )
