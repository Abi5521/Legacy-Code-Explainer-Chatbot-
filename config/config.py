import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_MODEL_NAME = "llama-3.1-8b-instant"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

if not GROQ_API_KEY:
    print("WARNING: GROQ_API_KEY is not set in the environment variables. Please update your .env file.")