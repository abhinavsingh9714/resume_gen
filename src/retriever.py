import json
import faiss
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
from config import KB_CHUNK_FILE, FAISS_INDEX_PATH, EMBEDDING_MODEL

class KnowledgeBaseRetriever:
    def __init__(self):
        self.model = SentenceTransformer(EMBEDDING_MODEL)
        self.kb_jsonl_path = KB_CHUNK_FILE
        self.faiss_index_path = FAISS_INDEX_PATH

        self.entries = self._load_kb_entries()
        self.index = self._load_faiss_index()

    def _load_kb_entries(self):
        entries = []
        with self.kb_jsonl_path.open("r", encoding="utf-8") as f:
            for line in f:
                entries.append(json.loads(line))
        return entries

    def _load_faiss_index(self):
        return faiss.read_index(str(self.faiss_index_path))

    def retrieve(self, query: str, top_k: int = 3):
        query_embedding = self.model.encode([query]).astype("float32")
        distances, indices = self.index.search(query_embedding, top_k)
        return [self.entries[i] for i in indices[0] if i < len(self.entries)]