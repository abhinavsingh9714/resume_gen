import json
import faiss
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain.schema import Document
from langchain.embeddings import HuggingFaceEmbeddings
from src.config import KB_CHUNK_FILE, FAISS_INDEX_PATH, EMBEDDING_MODEL

class KnowledgeBaseRetriever:
    def __init__(self,top_k:3):
        index = faiss.read_index(str(FAISS_INDEX_PATH))

        chunk_entries = self._load_kb_entries()
        
        docstore = self._create_docstore(chunk_entries)
        index_to_docstore_id = {i: str(i) for i in range(len(chunk_entries))}

        self.embedding = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

        self.vectorstore = FAISS(
            embedding_function = self.embedding,
            index = index,
            docstore = docstore,
            index_to_docstore_id = index_to_docstore_id
        )

        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": top_k})

    def _load_kb_entries(self):
        chunk_entries = []
        with KB_CHUNK_FILE.open("r", encoding="utf-8") as f:
            for line in f:
                entry = json.loads(line)
                chunk_entries.append(entry)
        return chunk_entries

    def _create_docstore(self,chunk_entries):
        docstore = InMemoryDocstore({str(i): Document(page_content=entry['content'], metadata=entry.get('metadata',{})) for i,entry in enumerate(chunk_entries)} )
        return docstore

    def retrieve(self, query: str):
        retrieved_docs = self.retriever.invoke(query)
        return [d.page_content for d in retrieved_docs]
    

if __name__ == "__main__":
    retriever = KnowledgeBaseRetriever(1)
    print('\n\n',retriever.retrieve('write a great professional resume for a machine learning engineer'))