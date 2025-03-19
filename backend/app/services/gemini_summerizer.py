import requests
import logging
from dataclasses import dataclass
from typing import List, Optional, Dict
from app.config import GENAI_API_KEY


logger = logging.getLogger(__name__)
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"


@dataclass
class GeminiResponse:
    text: str

    @staticmethod
    def from_response(response: Dict) -> Optional["GeminiResponse"]:
        candidates: List[Dict] = response.get("candidates", [])
        if not candidates:
            return None

        content_parts = candidates[0].get("content", {}).get("parts", [])
        if not content_parts:
            return None

        summary_text = content_parts[0].get("text", "").strip()
        return GeminiResponse(summary_text) if summary_text else None


class GeminiAPIError(Exception):
    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code


def summarize_text(text: str) -> str:
    headers = {"Content-Type": "application/json"}
    params = {"key": GENAI_API_KEY}

    prompt = (
            "Read the following text and provide a concise, yet complete summary "
            "that captures all key details. Avoid adding opinions or extra commentary. "
            "Respond only with the summary:\n\n" + text
    )

    data = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        logger.debug(f"Sending text to Gemini API: {data}")
        response = requests.post(GEMINI_URL, json=data, headers=headers, params=params, timeout=10)
        response.raise_for_status()

        try:
            result = response.json()
        except ValueError:
            raise GeminiAPIError(f"Invalid JSON response: {response.text}", response.status_code)

        summary = GeminiResponse.from_response(result)
        if not summary:
            raise GeminiAPIError(f"Empty or malformed response: {result}", response.status_code)

        return summary.text

    except requests.Timeout:
        logger.error("Gemini API request timed out.")
        return "API request timed out"
    except requests.RequestException as e:
        logger.error(f"Gemini API error: {e}. Request data: {data}")
        return "Generation failed"
    except GeminiAPIError as e:
        logger.error(f"Gemini API response error: {e}. Status code: {e.status_code}")
        return "API response error"
