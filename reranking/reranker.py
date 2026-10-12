from sentence_transformers import CrossEncoder

model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
def rerank(query, retrieved_chunks, top_n=3):
    pairs = [(query, chunk["text"]) for chunk in retrieved_chunks]
    scores = model.predict(pairs)
    for chunk, score in zip(retrieved_chunks, scores):
        chunk["score"] = score

    retrieved_chunks.sort(key=lambda chunk: chunk["score"], reverse=True)
    return retrieved_chunks[:top_n]