# datachat/pdf_query.py
import faiss
import pickle
import torch
from sentence_transformers import SentenceTransformer
import google.generativeai as genai

INDEX_PATH = "pdf_index.faiss"
META_PATH = "pdf_chunks.pkl"
MODEL_NAME = "all-MiniLM-L6-v2"

# ----------------- Safe model load -----------------
device = "cuda" if torch.cuda.is_available() else "cpu"

try:
    model = SentenceTransformer(MODEL_NAME, device=device)
except NotImplementedError:
    model = SentenceTransformer(MODEL_NAME)
    model.to_empty(device)

# ----------------- Load FAISS index & chunks once -----------------
index = faiss.read_index(INDEX_PATH)

with open(META_PATH, "rb") as f:
    chunks = pickle.load(f)


def query_pdf(question: str, k=5):
    # Encode question
    q_embedding = model.encode([question])
    if hasattr(q_embedding, "cpu"):  # convert tensor to numpy if needed
        q_embedding = q_embedding.cpu().numpy()

    # Search FAISS
    _, indices = index.search(q_embedding, k)

    # Build context
    context = "\n\n".join(chunks[i] for i in indices[0])

    # Build prompt
    prompt = f"""
You are answering strictly from the context below.
If the answer is not present, say "Not found in document".

CONTEXT:
{context}

QUESTION:
{question}
"""

    # Generate response
    try:
        response = genai.GenerativeModel("models/gemini-flash-latest").generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating response: {str(e)}"
