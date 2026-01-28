import json
import re
from utils.logger import setup_logger

logger = setup_logger("parser")

def extract_json(text: str):
    """
    Extract JSON array from Gemini output.
    Handles markdown fences and stray text.
    """
    try:
        # Remove markdown fences
        cleaned = re.sub(r"```json|```", "", text).strip()
        return json.loads(cleaned)
    except Exception as e:
        logger.error(f"Failed to parse Gemini JSON: {e}")
        return []
