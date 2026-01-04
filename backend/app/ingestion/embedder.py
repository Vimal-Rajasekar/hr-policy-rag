# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from tqdm import tqdm
# import time

# def embed_documents(chunks, batch_size=10):
#     embedder = GoogleGenerativeAIEmbeddings(
#         model="models/embedding-001"
#     )

#     embedded_chunks = []

#     for i in tqdm(range(0, len(chunks), batch_size)):
#         batch = chunks[i:i + batch_size]
#         embedded_chunks.extend(batch)
#         time.sleep(1)  # rate-limit protection

#     return embedder, embedded_chunks
# Above function will be suitable when pinecone internally handles embedding call.
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from tqdm import tqdm
import time

def embed_documents(chunks, batch_size=10):
    embedder = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001"
    )

    texts = [doc.page_content for doc in chunks]
    metadatas = [doc.metadata for doc in chunks]

    embeddings = []

    for i in tqdm(range(0, len(texts), batch_size)):
        batch_texts = texts[i:i + batch_size]
        print(f"Embedding batch : {batch_texts}")
        batch_embeddings = embedder.embed_documents(batch_texts)
        embeddings.extend(batch_embeddings)
        time.sleep(1)  # free-tier protection
    print(f"Generated {len(embeddings)} embeddings.")

    return embeddings, texts, metadatas
