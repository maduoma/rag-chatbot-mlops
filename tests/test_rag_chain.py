# tests/test_rag_chain.py

from app.llm.rag_chain import RAGPipeline

def test_rag_pipeline():
    rag = RAGPipeline()
    result = rag.run("What is AI?")
    assert isinstance(result, str)
    assert "AI" in result or "context" in result
