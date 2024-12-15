
from langchain_openai import OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore

from dotenv import load_dotenv
import os

class VectorStore:
    def __init__(self, create=False):
        self.create = create
        load_dotenv()  # Load environment variables from .env file
        self.api_key = os.getenv("OPENAI_API_KEY")
        print("API key",self.api_key)
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        if self.create:    
            self.vector_store = InMemoryVectorStore(self.embeddings)
        else:
            self.vector_store = InMemoryVectorStore(self.embeddings).load(path="./vec_store", embedding = self.embeddings)
            
    def get_embedder(self):
        return self.embeddings