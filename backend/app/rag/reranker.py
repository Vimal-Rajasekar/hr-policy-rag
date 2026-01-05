from langchain_google_genai import GoogleGenerativeAI
import os

from dotenv import load_dotenv
load_dotenv()

class Reranker:
    def __init__(self):
        self.llm = GoogleGenerativeAI(
            model="gemini-2.5-flash-lite",
            api_key=os.getenv("GOOGLE_API_KEY")
        )

    def rerank(self, query: str, docs: list):
        """
        docs: List[langchain.schema.Document]
        Returns: top 5 most relevant documents
        """

        scored_docs = []

        for doc in docs:
            prompt = f"""
                Rank the relevance of this document to the query "{query}" from 0 to 1.

                Document:
                {doc.page_content}

                Respond with ONLY a number.
                """
            try:
                score = float(self.llm.predict(prompt))
            except Exception:
                score = 0.0

            scored_docs.append((score, doc))

        scored_docs.sort(key=lambda x: x[0], reverse=True)

        return [doc for _, doc in scored_docs[:5]]

