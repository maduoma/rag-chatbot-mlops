# tests/test_rag_chain.py
"""
Unit-test the RAG pipeline without hitting Anthropic or OpenAI.

We patch app.llm.generator._call_claude to return a deterministic
string.  That covers whichever LLM path the generator chooses.
"""

from unittest.mock import patch
from app.llm.rag_chain import RAGPipeline


@patch("app.llm.generator._call_claude", return_value="Mocked answer")
@patch("app.llm.generator.openai.ChatCompletion.create")
def test_rag_pipeline(mock_openai_create, mock_claude_call):
    # OpenAI stub (kept for completeness; not exercised when Claude branch chosen)
    mock_openai_create.return_value = type(
        "Resp",
        (),
        {
            "choices": [
                type("Choice", (), {"message": {"content": "Mocked answer"}})()
            ]
        },
    )()

    rag = RAGPipeline()
    result = rag.run("What is AI?")

    assert result == "Mocked answer"
