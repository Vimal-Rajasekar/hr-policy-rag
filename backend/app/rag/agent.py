from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from pinecone import Pinecone
import os
from dotenv import load_dotenv
load_dotenv()

import logging
logger = logging.getLogger(__name__)
from backend.app.rag.reranker import Reranker

reranker = Reranker()

class PolicyAgent:
    def __init__(self):
        # Validate required environment variables up front for clearer errors
        required = {
            "GOOGLE_API_KEY": os.getenv("GOOGLE_API_KEY"),
            "PINECONE_API_KEY": os.getenv("PINECONE_API_KEY"),
            "PINECONE_INDEX": os.getenv("PINECONE_INDEX"),
        }
        missing = [k for k, v in required.items() if not v]
        if missing:
            raise ValueError(f"Missing environment variables: {', '.join(missing)}")

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-lite",
            temperature=0,
            api_key=required["GOOGLE_API_KEY"]
        )

        self.embedder = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001"
        )

        pc = Pinecone(api_key=required["PINECONE_API_KEY"])
        index = pc.Index(required["PINECONE_INDEX"])

        self.vectorstore = PineconeVectorStore(
            index=index,
            embedding=self.embedder,
            namespace="policies"
        )

        self.retriever = self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 6}
        )

        self.prompt = ChatPromptTemplate.from_template(
            """
            You are an internal HR policy assistant.

            RULES:
            - Answer ONLY using the provided context
            - If the answer is not in the context, say:
            "I could not find this information in the company policy documents."

            <context>
            {context}
            </context>

            Question: {question}
            """
        )

        self.chain = (
            self.prompt
            | self.llm
            | StrOutputParser()
        )

    def run(self, question: str) -> str:
        # Try to use the retriever API, but include a compatibility fallback for
        # retriever implementations that don't expose `get_relevant_documents`.
        try:
            # `similarity_search` typically accepts (query, k)
            docs = self.vectorstore.similarity_search(question, k=5)
        
        except Exception as e:
            logger.exception(f"Unexpected error when retrieving documents {e}")
            raise

        if not docs:
            return "I could not find this information in the company policy documents."

        context = "\n\n".join(d.page_content for d in docs)

        return self.chain.invoke(
            {"context": context, "question": question}
        )

    
    def stream(self, question: str):
        """
        Stream the answer token-by-token for FastAPI StreamingResponse
        """
        try:
            docs = self.vectorstore.similarity_search(question, k=10)
            print(f"Retrieved {len(docs)} documents from vector store.")
            print("Documents:", docs[:2])
        except Exception as e:
            logger.exception(f"Retrieval failed: {e}")
            yield "I could not retrieve policy documents."
            return

        if not docs:
            yield "I could not find this information in the company policy documents."
            return

        print(f"Length of retrieved docs: {len(docs)}")
        reranked_docs = reranker.rerank(question, docs)
        print(f"Length of reranked docs: {len(reranked_docs)}")

        context = "\n\n".join(doc.page_content for doc in reranked_docs)


        prompt_text = self.prompt.format(
            context=context,
            question=question
        )

        # IMPORTANT: stream directly from the LLM
        for chunk in self.llm.stream(
            [HumanMessage(content=prompt_text)]
        ):
            if chunk:
                yield chunk
