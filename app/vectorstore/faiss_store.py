# app/vectorstore/faiss_store.py

import faiss
import os
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer

class LocalVectorStore:
    def __init__(self, index_path='data/faiss_index/index.faiss', model_name='all-MiniLM-L6-v2'):
        self.index_path = index_path
        self.embedding_model = SentenceTransformer(model_name)
        self.dim = self.embedding_model.get_sentence_embedding_dimension()
        self.index = faiss.IndexFlatL2(self.dim)
        self.texts = []

        self.meta_path = index_path.replace('.faiss', '_meta.pkl')
        self._load_index()

    def _load_index(self):
        if os.path.exists(self.index_path) and os.path.exists(self.meta_path):
            self.index = faiss.read_index(self.index_path)
            with open(self.meta_path, 'rb') as f:
                self.texts = pickle.load(f)

    def save_index(self):
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        faiss.write_index(self.index, self.index_path)
        with open(self.meta_path, 'wb') as f:
            pickle.dump(self.texts, f)

    def add_texts(self, texts):
        embeddings = self.embedding_model.encode(texts, convert_to_numpy=True)
        self.index.add(embeddings)
        self.texts.extend(texts)
        self.save_index()

    
    def search(self, query, k=3):
        if self.index.ntotal == 0:
            return ["[Vector store is empty. Please upload and index a document first.]"]

        query_vec = self.embedding_model.encode([query])
        D, I = self.index.search(query_vec, k)

        results = []
        for i in I[0]:
            if 0 <= i < len(self.texts):
                results.append(self.texts[i])
        return results if results else ["[No relevant results found.]"]