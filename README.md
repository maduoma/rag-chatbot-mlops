# rag-chatbot-mlops

# 🧠 RAG Chatbot (Retrieval-Augmented Generation)

A full-stack **AI-powered chatbot** that answers questions from your uploaded documents (PDF, CSV, DOCX, TXT) using **retrieval-augmented generation (RAG)**. Runs **100% locally** or optionally via OpenAI/Claude.

---

## 🚀 Features

- Upload documents and ask questions about them
- Built-in document chunking, embedding (FAISS + SBERT)
- LLM toggle: OpenAI, Claude, or Ollama (Mistral)
- Flask-based chat UI
- Dockerized + tested + CI/CD ready

---

## 🛠️ Tech Stack

- **Backend**: FastAPI + FAISS + SentenceTransformers
- **Frontend**: Flask
- **LLMs**: Mistral via Ollama | OpenAI | Claude (Anthropic)
- **Embeddings**: `all-MiniLM-L6-v2`
- **Testing**: `pytest`
- **Monitoring**: Prometheus-ready (optional)
- **CI**: GitHub Actions

---

## 📁 Project Structure

```bash
rag-chatbot/
├── app/
│   ├── ui/               # Flask frontend
│   ├── api/              # Optional FastAPI endpoints
│   ├── ingestion/        # File parsing & chunking
│   ├── vectorstore/      # FAISS logic
│   ├── llm/              # LLM integrations
│   ├── utils/            # Shared helpers
├── tests/                # Unit & integration tests
├── docker/               # Docker + docker-compose
├── data/                 # Uploaded files + indexes
