from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_chunks(chunks,document_name,batch_size=32):
    texts = [chunk["text"] for chunk in chunks]

    embeddings = model.encode(texts,batch_size=batch_size)

    embedded_chunks = []

    for chunk, embedding in zip(chunks, embeddings):
        embedded_chunk = {
            "chunk_id": f"{document_name}_{chunk['chunk_id']}",
            "page": chunk["page"],
            "text": chunk["text"],
            "document": document_name,
            "embedding": embedding
        }
        embedded_chunks.append(embedded_chunk)
    return embedded_chunks