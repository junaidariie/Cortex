import os
import logging
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

# 1. Setup Logging (Better than print for Servers)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

embeddings = OpenAIEmbeddings(model='text-embedding-3-small')

# 2. Add arguments for flexible paths
def Ingest_Data(pdf_path: str, vector_db_path: str = "vectorstore/db_faiss"):
    """
    Ingests a PDF, splits it, and saves the vector store.
    Returns a dict with status to send back to the Frontend.
    """
    try:
        logger.info(f"Starting ingestion for: {pdf_path}")

        # Validation: Check if file exists
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"The file {pdf_path} was not found.")

        # Load
        loader = PyPDFLoader(pdf_path)
        pages = loader.load_and_split()
        
        if not pages:
            return {"status": "error", "message": "PDF contains no text."}

        # Split
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=250)
        docs = splitter.split_documents(pages)
        logger.info(f"Processing {len(docs)} chunks...")

        # Embed & Save
        # Note: This is CPU/Network intensive. In FastAPI, 
        # ensure you run this in a BackgroundTask or ThreadPool.
        db = FAISS.from_documents(docs, embeddings) 
        db.save_local(vector_db_path)
        
        logger.info(f"Saved vectorstore to {vector_db_path}")

        # 3. Return JSON-friendly data
        return {
            "status": "success",
            "chunks_processed": len(docs),
            "db_path": vector_db_path,
            "message": "File successfully ingested and indexed."
        }

    except Exception as e:
        logger.error(f"Ingestion failed: {str(e)}")
        return {
            "status": "failed", 
            "error": str(e)
        }
    

    
#Ingest_Data("MLBOOK.pdf")