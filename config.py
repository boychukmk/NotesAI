from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
GENAI_API_KEY = os.getenv("GENAI_API_KEY")
