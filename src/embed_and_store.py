import json
import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from config import KB_CHUNK_FILE, FAISS_INDEX_PATH, EMBEDDING_MODEL, KB_INDEX_DIR

os.makedirs(KB_INDEX_DIR, exist_ok=True)

print("Loading embedding model...")
model = SentenceTransformer(EMBEDDING_MODEL)

print("Loading chunks...")
chunks = []
with open(KB_CHUNK_FILE, "r", encoding="utf-8") as f:
    for line in f:
        entry = json.loads(line)
        chunks.append(entry["content"])

print("Computing embeddings...")
embeddings = model.encode(chunks, show_progress_bar=True, convert_to_numpy=True)

print("Building FAISS index...")
d = embeddings.shape[1]
index = faiss.IndexFlatL2(d)
index.add(embeddings)

print("Saving index...")
faiss.write_index(index, str(FAISS_INDEX_PATH))
print(f"Saved FAISS index with {len(chunks)} entries")