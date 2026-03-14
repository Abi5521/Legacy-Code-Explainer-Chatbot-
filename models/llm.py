import logging
from langchain_groq import ChatGroq
from config.config import GROQ_API_KEY, GROQ_MODEL_NAME

logger = logging.getLogger(__name__)

def get_llm(temperature=0.0):
    if not GROQ_API_KEY:
        logger.error("GROQ_API_KEY is missing. Cannot initialize LLM.")
        return None
        
    try:
        llm = ChatGroq(
            temperature=temperature,
            groq_api_key=GROQ_API_KEY,
            model_name=GROQ_MODEL_NAME
        )
        return llm
    except Exception as e:
        logger.error(f"Error initializing LLM: {e}")
        return None