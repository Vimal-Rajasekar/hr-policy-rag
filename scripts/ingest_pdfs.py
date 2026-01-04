import sys
from pathlib import Path

# --- Add project root for imports ---
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))  # ensures backend/ is importable

from backend.app.ingestion.loader import load_pdfs
from backend.app.ingestion.chunker import chunk_documents
from backend.app.ingestion.embedder import embed_documents
from backend.app.ingestion.pinecone_store import store_embeddings
from dotenv import load_dotenv
import os
load_dotenv()

PDF_FOLDER = os.getenv("PDF_PATH", "data/policies")

def run():
    docs = load_pdfs(PDF_FOLDER)
    chunks = chunk_documents(docs)
    print(f"Total chunks created: {len(chunks)}")
    print("Sample chunk content:", chunks[0].page_content if chunks else "No chunks created")
    embeddings, texts, metadatas = embed_documents(chunks)

    store_embeddings(
        embeddings=embeddings,
        texts=texts,
        metadatas=metadatas
    )
    print("Ingestion and storage complete.")


if __name__ == "__main__":
    run()
