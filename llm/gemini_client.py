import os
from dotenv import load_dotenv
from utils.logger import setup_logger
from llm.prompts import VISION_PROMPT
import config
from google import genai
from PIL import Image

load_dotenv()
logger = setup_logger("gemini_client")


class GeminiClient:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not set in environment")

        self.client = genai.Client(api_key=api_key)
        self.model_name = config.GEMINI_VISION_MODEL

        logger.info("Gemini client initialized")

    def analyze_frames(self, frames: list[Image.Image], session_id: str) -> str:
        logger.info(f"[session={session_id}] Preparing content for Gemini")

        contents = [VISION_PROMPT]

        valid_images = 0
        for img in frames:
            if not isinstance(img, Image.Image):
                logger.warning(
                    f"[session={session_id}] Skipping non-image frame: {type(img)}"
                )
                continue

            contents.append(img)
            valid_images += 1

        logger.info(
            f"[session={session_id}] Added {valid_images}/{len(frames)} images to Gemini input"
        )

        if valid_images == 0:
            logger.warning(
                f"[session={session_id}] No valid images provided to Gemini"
            )
            return ""

        logger.info(f"[session={session_id}] Sending request to Gemini Vision")

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=contents,
        )

        logger.info(f"[session={session_id}] Gemini response received")

        if response.text:
            logger.info(f"[session={session_id}] ===== GEMINI RAW RESPONSE START =====")
            logger.info(response.text)
            logger.info(f"[session={session_id}] ===== GEMINI RAW RESPONSE END =====")
        else:
            logger.warning(f"[session={session_id}] Gemini returned empty response")

        return response.text or ""
        
