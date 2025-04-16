import os
import faiss
import json
import openai
import numpy as np
from langchain.embeddings import OpenAIEmbeddings

openai.api_key = os.getenv("OPENAI_API_KEY")

class VectorStore:
    def __init__(self, dim=1536):
        self.dim = dim
        self.index = faiss.IndexFlatL2(dim)
        self.metadata = []
        self.embedding_model = OpenAIEmbeddings(model="text-embedding-ada-002")

    def add(self, record, uid):
        content = json.dumps(record, ensure_ascii=False)
        embedding = self.embedding_model.embed_query(content)
        self.index.add(np.array([embedding], dtype=np.float32))
        self.metadata.append({"uid": uid, "data": record})

    def save_index(self, index_path, metadata_path):
        faiss.write_index(self.index, index_path)
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(self.metadata, f, indent=2, ensure_ascii=False)
