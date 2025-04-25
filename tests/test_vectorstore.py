# tests/test_vectorstore.py

from app.vectorstore.faiss_store import LocalVectorStore

def test_vector_store_add_and_search(tmp_path):
    store = LocalVectorStore(index_path=str(tmp_path / "test_index.faiss"))
    docs = ["The cat sat on the mat.", "The quick brown fox.", "AI is transforming tech."]
    store.add_texts(docs)

    results = store.search("cat")
    assert isinstance(results, list)
    assert len(results) > 0
