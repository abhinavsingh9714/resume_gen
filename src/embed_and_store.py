import json
import os
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle

# Paths
CHUNK_FILE = "resume_gen/kb_chunks/knowledge_base.jsonl"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
FAISS_INDEX_PATH = "resume_gen/kb_index/faiss.index"
# METADATA_PATH = "resume_gen/kb_index/metadata.pkl"

# Ensure output directory exists
os.makedirs("kb_index", exist_ok=True)

# Load embedding model
print("🔍 Loading embedding model...")
model = SentenceTransformer(EMBEDDING_MODEL)

# Load knowledge base chunks
print("📄 Loading chunks...")
chunks = []
# metadata = []

with open(CHUNK_FILE, "r", encoding="utf-8") as f:
    for line in f:
        entry = json.loads(line)
        chunks.append(entry["content"])
        # metadata.append({"source": entry["source"], "tags": entry.get("tags", [])})

# Compute embeddings
print("⚙️  Computing embeddings...")
embeddings = model.encode(chunks, show_progress_bar=True, convert_to_numpy=True)

# Build FAISS index
print("📦 Building FAISS index...")
d = embeddings.shape[1]  # embedding dimension
index = faiss.IndexFlatL2(d)
index.add(embeddings)

# Save index and metadata
print("💾 Saving index and metadata...")
faiss.write_index(index, FAISS_INDEX_PATH)
# with open(METADATA_PATH, "wb") as f:
#     pickle.dump(metadata, f)

print(f"✅ Saved FAISS index with {len(chunks)} documents")