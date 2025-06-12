import os
import json
from pathlib import Path

INPUT_DIR = "resume_gen/knowledge_base"  # Replace with the path to your 19 txt files
OUTPUT_FILE = "resume_gen/kb_chunks/knowledge_base.jsonl"
CHUNK_SIZE = 128  # Adjust if needed (in characters)

def chunk_text(text, max_len=CHUNK_SIZE):
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks = []
    buffer = ""

    for para in paragraphs:
        if len(buffer) + len(para) < max_len:
            buffer += " " + para
        else:
            chunks.append(buffer.strip())
            buffer = para
    if buffer:
        chunks.append(buffer.strip())

    return chunks

def process_files():
    kb_entries = []

    for file_path in Path(INPUT_DIR).glob("*.txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        chunks = chunk_text(text)
        for chunk in chunks:
            kb_entries.append({
                "content": chunk,
            })

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for entry in kb_entries:
            json.dump(entry, f)
            f.write("\n")

    print(f"✅ Processed {len(kb_entries)} chunks into {OUTPUT_FILE}")

if __name__ == "__main__":
    process_files()
