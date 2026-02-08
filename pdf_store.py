# datachat/pdf_store.py
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import faiss
import os
import pickle

MODEL_NAME = "all-MiniLM-L6-v2"
INDEX_PATH = "pdf_index.faiss"
META_PATH = "pdf_chunks.pkl"

model = SentenceTransformer(MODEL_NAME)


def load_pdf_text(path: str) -> str:
    reader = PdfReader(path)
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def chunk_text(text, chunk_size=500, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


def ingest_pdf(path: str):
    text = load_pdf_text(path)
    chunks = chunk_text(text)

    embeddings = model.encode(chunks)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, INDEX_PATH)

    with open(META_PATH, "wb") as f:
        pickle.dump(chunks, f)
