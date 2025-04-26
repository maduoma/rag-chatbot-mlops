# tests/test_rag_chain.py
import pytest
from unittest.mock import patch
from app.llm.rag_chain import RAGPipeline



@patch("app.llm.generator._call_claude", return_value="Mocked answer")
@patch("app.llm.generator.openai.ChatCompletion.create")
def test_rag_pipeline(mock_create):
    mock_create.return_value = {"choices": [{"message": {"content": "Mocked answer"}}]}
    rag = RAGPipeline()

    # ----- Act ---------------------------------------------------------------
    result = rag.run("What is AI?")
    assert "Mocked answer" in result
# from app.llm.rag_chain import RAGPipeline

# def test_rag_pipeline():
#     rag = RAGPipeline()
#     result = rag.run("What is AI?")
#     assert isinstance(result, str)
#     assert "AI" in result or "context" in result
