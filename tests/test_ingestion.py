# tests/test_ingestion.py

import os
from app.ingestion.document_loader import load_document
from app.ingestion.chunker import split_text

def test_pdf_loading():
    path = "tests/sample_data/sample.pdf"
    text = load_document(path)
    assert isinstance(text, str) and len(text) > 0

def test_chunking():
    text = "This is a test.\n" * 100
    chunks = split_text(text, max_chunk_size=100)
    assert all(len(c) <= 100 for c in chunks)
    assert isinstance(chunks, list)
