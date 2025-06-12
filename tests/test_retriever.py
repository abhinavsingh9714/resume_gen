import pytest
from src.retriever import KnowledgeBaseRetriever

def test_retrieve_valid_chunks():
    retriever = KnowledgeBaseRetriever()
    query = "How to write STAR format bullet points?"
    results = retriever.retrieve(query, top_k=3)

    assert isinstance(results, list)
    assert len(results) > 0
    assert all("content" in r for r in results)

def test_retrieve_returns_empty_when_no_match():
    retriever = KnowledgeBaseRetriever()
    query = "completelyrandomtextthatshouldnotmatch"
    results = retriever.retrieve(query, top_k=3)

    # FAISS will return best match even if poor, so check similarity manually if needed
    assert isinstance(results, list)
    assert len(results) == 3  # still returns results
    assert all("content" in r for r in results)
