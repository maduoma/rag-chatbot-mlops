# app/ingestion/document_loader.py

import os
import fitz  # PyMuPDF
import csv
import docx
from typing import List

def load_text_file(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def load_pdf(file_path: str) -> str:
    doc = fitz.open(file_path)
    text = "\n".join([page.get_text() for page in doc])
    return text

def load_csv(file_path: str) -> str:
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        return "\n".join([", ".join(row) for row in reader])

def load_docx(file_path: str) -> str:
    doc = docx.Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs])

def load_document(file_path: str) -> str:
    if file_path.endswith('.pdf'):
        return load_pdf(file_path)
    elif file_path.endswith('.txt'):
        return load_text_file(file_path)
    elif file_path.endswith('.csv'):
        return load_csv(file_path)
    elif file_path.endswith('.docx'):
        return load_docx(file_path)
    else:
        raise ValueError("Unsupported file format.")
