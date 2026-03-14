import logging
from langchain_huggingface import HuggingFaceEmbeddings
from config.config import EMBEDDING_MODEL_NAME

logger = logging.getLogger(__name__)

def get_embeddings():
    try:
        embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
        return embeddings
    except Exception as e:
        logger.error(f"Error initializing embeddings model: {e}")
        return None