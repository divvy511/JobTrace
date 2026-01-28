from storage.job_actions import JobAction
from utils.logger import setup_logger

logger = setup_logger("validator")

MIN_CONFIDENCE = 0.6

def validate_actions(raw_actions: list) -> list[JobAction]:
    valid = []

    for item in raw_actions:
        try:
            action = JobAction(**item)

            if action.confidence is not None and action.confidence < MIN_CONFIDENCE:
                logger.warning(
                    f"Action skipped due to low confidence: {action.confidence}"
                )
                continue

            valid.append(action)

        except Exception as e:
            logger.warning(f"Invalid action skipped: {item} | {e}")

    return valid
