def chunk_pages(pages, chunk_size=100, overlap=20):

    if overlap >= chunk_size:
         raise ValueError("overlap must be smaller than chunk_size")
    
    chunks = []

    for page in pages:
        text = page["text"]
        page_number = page["page"]
        
        if not text.strip():
            continue

        words = text.split()
        start = 0

        while start < len(words):
            end = start + chunk_size
            chunk_words = words[start:end]
            chunk_text = " ".join(chunk_words)
            
            chunk = {
                "chunk_id": f"page_{page_number}_chunk_{len(chunks)}",
                "page": page_number,
                "text": chunk_text
            }

            chunks.append(chunk)
            start = end - overlap
    return chunks