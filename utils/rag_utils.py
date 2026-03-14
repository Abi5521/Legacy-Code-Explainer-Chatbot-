import logging
from langchain_community.vectorstores import FAISS

logger = logging.getLogger(__name__)

def get_vectorstore(chunks, embeddings):
    try:
        if not chunks:
            logger.warning("No chunks provided to create vectorstore.")
            return None
            
        vectorstore = FAISS.from_documents(chunks, embeddings)
        return vectorstore
    except Exception as e:
        logger.error(f"Error creating FAISS vectorstore: {e}")
        return None

def get_retriever(vectorstore):
    try:
        if not vectorstore:
            return None
        retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
        return retriever
    except Exception as e:
        logger.error(f"Error creating retriever: {e}")
        return None
