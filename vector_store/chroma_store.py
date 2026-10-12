import chromadb

client = chromadb.PersistentClient(path="data/chroma")
collection = client.get_or_create_collection(name="omniscIa")

def add_chunks(embedded_chunks):
    ids = [chunk["chunk_id"] for chunk in embedded_chunks]
    documents = [chunk["text"] for chunk in embedded_chunks]
    metadatas = [
        {
            "document": chunk["document"],
            "page": chunk["page"]
        }
        for chunk in embedded_chunks
    ]
    embeddings = [chunk["embedding"].tolist() for chunk in embedded_chunks]
    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )
    

def get_count():
    return collection.count()