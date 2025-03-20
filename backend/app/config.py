from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL","postgresql+asyncpg://user:password@db:5432/notes_db")
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL","sqlite+aiosqlite:///:memory:")
GENAI_API_KEY = os.getenv("GENAI_API_KEY")
if not GENAI_API_KEY:
    raise ValueError("Gemini API Key is not set in the environment variables")
