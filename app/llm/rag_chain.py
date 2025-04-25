# app/llm/rag_chain.py

from app.vectorstore.faiss_store import LocalVectorStore
from app.llm.generator import generate_answer

class RAGPipeline:
    def __init__(self):
        self.store = LocalVectorStore()

    def run(self, query: str) -> str:
        retrieved_chunks = self.store.search(query)
        context = "\n\n".join(retrieved_chunks)
        return generate_answer(context, query)
