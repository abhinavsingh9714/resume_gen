import os
import json
from pathlib import Path
from config import KB_INPUT_DIR, KB_CHUNK_FILE
import spacy

# Load spaCy's small English model
nlp = spacy.load("en_core_web_sm")

CHUNK_SIZE = 512  # Adjust based on optimal retrieval behavior

def chunk_text_paragraph(text, max_len=CHUNK_SIZE):
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

def sliding_window_chunker(text, window_size=4, stride=2, max_tokens=CHUNK_SIZE):
    """
    Splits text into sentence-based overlapping chunks using spaCy.
    Each chunk contains `window_size` sentences with `stride` overlap.
    """
    doc = nlp(text)
    sentences = [sent.text.strip() for sent in doc.sents if sent.text.strip()]

    chunks = []
    i = 0
    while i < len(sentences):
        window = sentences[i:i + window_size]
        chunk = " ".join(window).strip()
        if len(chunk) > 0:
            chunks.append(chunk)
        i += stride

    return chunks


def process_files():
    os.makedirs(KB_CHUNK_FILE.parent, exist_ok=True)
    kb_entries = []

    for file_path in Path(KB_INPUT_DIR).glob("*.txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        chunks = sliding_window_chunker(text, window_size=4, stride=2, max_tokens=CHUNK_SIZE)
        for chunk in chunks:
            kb_entries.append({"content": chunk})

    with open(KB_CHUNK_FILE, "w", encoding="utf-8") as f:
        for entry in kb_entries:
            json.dump(entry, f)
            f.write("\n")

    print(f"Processed {len(kb_entries)} chunks into {KB_CHUNK_FILE}")

if __name__ == "__main__":
    process_files()
