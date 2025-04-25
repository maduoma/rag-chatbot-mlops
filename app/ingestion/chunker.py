# app/ingestion/chunker.py

from typing import List

def split_text(text: str, max_chunk_size: int = 500) -> List[str]:
    paragraphs = text.split('\n')
    chunks = []
    chunk = ""

    for para in paragraphs:
        if len(chunk) + len(para) < max_chunk_size:
            chunk += para + "\n"
        else:
            chunks.append(chunk.strip())
            chunk = para + "\n"

    if chunk:
        chunks.append(chunk.strip())

    return chunks
