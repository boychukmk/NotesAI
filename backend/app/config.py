from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
GENAI_API_KEY = os.getenv("GENAI_API_KEY")
if not GENAI_API_KEY or not DATABASE_URL:
    raise ValueError("Database URL ot Gemini API Key are not set in the environment variables")
