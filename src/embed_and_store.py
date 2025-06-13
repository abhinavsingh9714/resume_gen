import os
import json
import re
import faiss
import numpy as np
from typing import List
from sentence_transformers import SentenceTransformer
from config import KB_CHUNK_FILE, FAISS_INDEX_PATH, EMBEDDING_MODEL, KB_INDEX_DIR


def setup_directories():
    """Ensure necessary directories exist."""
    os.makedirs(KB_INDEX_DIR, exist_ok=True)


def load_embedding_model(model_name: str) -> SentenceTransformer:
    """Load and return the sentence transformer model."""
    print("Loading embedding model...")
    return SentenceTransformer(model_name)


def clean_text(text: str) -> str:
    """Normalize whitespace and strip control characters."""
    text = text.replace("\n", " ").replace("\r", " ")
    return re.sub(r"\s+", " ", text).strip()


def load_chunks(file_path: str) -> List[str]:
    """Load and clean text chunks from a JSONL file."""
    print("Loading and cleaning chunks...")
    cleaned_chunks = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            entry = json.loads(line)
            cleaned_chunks.append(clean_text(entry["content"]))
    return cleaned_chunks


def compute_embeddings(model: SentenceTransformer, texts: List[str]) -> np.ndarray:
    """Generate embeddings for the given list of texts."""
    print("Computing embeddings...")
    return model.encode(texts, show_progress_bar=True, convert_to_numpy=True)


def build_faiss_index(embeddings: np.ndarray) -> faiss.IndexFlatL2:
    """Build a FAISS index from embeddings."""
    print("Building FAISS index...")
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    return index


def save_index(index: faiss.IndexFlatL2, index_path: str):
    """Save the FAISS index to disk."""
    print(f"Saving index to {index_path}...")
    faiss.write_index(index, str(index_path))
    print(f"Saved FAISS index with {index.ntotal} entries.")


def main():
    setup_directories()
    model = load_embedding_model(EMBEDDING_MODEL)
    chunks = load_chunks(KB_CHUNK_FILE)
    embeddings = compute_embeddings(model, chunks)
    index = build_faiss_index(embeddings)
    save_index(index, FAISS_INDEX_PATH)


if __name__ == "__main__":
    main()