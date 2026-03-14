import logging
from langchain_text_splitters import RecursiveCharacterTextSplitter
import tempfile
import os

logger = logging.getLogger(__name__)

def process_uploaded_file(uploaded_file):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name

        with open(tmp_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
            
        os.remove(tmp_path)
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        chunks = text_splitter.create_documents(
            texts=[text], 
            metadatas=[{"source": uploaded_file.name}]
        )
        
        return chunks
    except Exception as e:
        logger.error(f"Error processing file {uploaded_file.name}: {e}")
        return []
