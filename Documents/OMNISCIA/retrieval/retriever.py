import chromadb
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="data/chroma")
collection = client.get_collection(name="omniscIa")


def retrieve(query, top_k=3, document_name=None):
    query_embedding = model.encode(query)

    where = None
    if document_name:
        where = {"document": document_name}

    try:
        results = collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=top_k,
            where=where
        )
    except Exception as e:
        raise RuntimeError(f"Vector search failed: {e}") from e

    if not results["distances"] or not results["distances"][0]:
        return []

    retrieved_chunks = []

    for i in range(len(results["documents"][0])):
        distance = results["distances"][0][i]

        # Reject chunks whose distance exceeds the threshold
        if distance > 0.8:
            continue

        chunk = {
            "text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": distance
        }

        retrieved_chunks.append(chunk)

    return retrieved_chunks
