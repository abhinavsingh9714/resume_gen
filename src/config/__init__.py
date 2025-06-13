from pathlib import Path

# Root directory (can be changed if needed)
ROOT_DIR = Path(__file__).resolve().parent.parent.parent

# Paths
KB_INPUT_DIR = ROOT_DIR / "knowledge_base"             # Folder with .txt files
KB_CHUNK_FILE = ROOT_DIR / "kb_chunks" / "knowledge_base.jsonl"
KB_INDEX_DIR = ROOT_DIR / "kb_index"
FAISS_INDEX_PATH = KB_INDEX_DIR / "faiss.index"
# METADATA_PATH = KB_INDEX_DIR / "metadata.pkl"        # Optional if use metadata

# Embedding Model
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Gemini LLM model
GEMINI_MODEL = "models/gemini-1.5-flash"