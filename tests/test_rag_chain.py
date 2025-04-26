# tests/test_rag_chain.py
"""
Unit test for the RAGPipeline that verifies the end-to-end call chain
without requiring a real OpenAI API key.

We stub openai.ChatCompletion.create so that app/llm/generator._call_openai
receives an object that matches the SDK’s real response shape:
    response.choices[0].message["content"]
"""

from types import SimpleNamespace
from unittest.mock import patch

from app.llm.rag_chain import RAGPipeline


@patch("app.llm.generator.openai.ChatCompletion.create")
def test_rag_pipeline(mock_create):
    """
    Given a mocked OpenAI response
    When RAGPipeline.run() is invoked
    Then it should return the assistant message content unaltered.
    """
    # ----- Arrange -----------------------------------------------------------
    mock_create.return_value = SimpleNamespace(
        choices=[
            SimpleNamespace(
                message={"content": "Mocked answer"}
            )
        ]
    )

    rag = RAGPipeline()

    # ----- Act ---------------------------------------------------------------
    result = rag.run("What is AI?")

    # ----- Assert ------------------------------------------------------------
    assert result == "Mocked answer"
