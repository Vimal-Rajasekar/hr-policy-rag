# from pinecone import Pinecone
# from langchain_community.vectorstores import Pinecone as PineconeStore
# import os

# def store_embeddings(embedder, documents):
#     pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

#     index = pc.Index(os.getenv("PINECONE_INDEX"))

#     PineconeStore.from_documents(
#         documents=documents,
#         embedding=embedder,
#         index_name=os.getenv("PINECONE_INDEX"),
#         namespace="policies"
#     )

#Above function will be suitable when pinecone internally handles embedding call.
from pinecone import Pinecone, ServerlessSpec
import os
import uuid

def store_embeddings(embeddings, texts, metadatas, namespace="policies"):
    pc = Pinecone(
        api_key=os.environ.get("PINECONE_API_KEY")
    )
    index = pc.Index(
        name=os.getenv("PINECONE_INDEX"),
        host=os.getenv("PINECONE_HOST")
    )

    vectors = []
    for emb, text, meta in zip(embeddings, texts, metadatas):
        vectors.append({
            "id": str(uuid.uuid4()),
            "values": emb,
            "metadata": {
                **meta,
                "text": text
            }
        })

    index.upsert(vectors=vectors, namespace=namespace)
    print(f"Stored {len(vectors)} embeddings in Pinecone index '{os.getenv('PINECONE_INDEX')}' under namespace '{namespace}'.")