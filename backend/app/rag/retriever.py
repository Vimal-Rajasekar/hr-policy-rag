from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Pinecone
import os

class PolicyRetriever:
    def __init__(self, top_k=5):
        self.embedder = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
        self.index_name = os.getenv("PINECONE_INDEX")
        self.namespace = "policies"
        self.top_k = top_k

    def retrieve(self, query: str):
        # Embed query
        query_vec = self.embedder.embed_query(query)

        # Connect to Pinecone index
        pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        index = pc.Index(name=self.index_name)

        # Retrieve top K
        result = index.query(
            vector=query_vec,
            top_k=self.top_k,
            namespace=self.namespace,
            include_metadata=True
        )
        return result['matches']
