
from pathlib import Path

from ingestion.pdf_loader import load_pdf
from chunking.text_chunking import chunk_pages
from embeddings.embedder import embed_chunks
from vector_store.chroma_store import add_chunks, get_count

from retrieval.retriever import retrieve
from reranking.reranker import rerank
from generation.generator import generate_answer


def ingest_document():
    """Extract, chunk, embed, and store a PDF document."""

    pdf_path = input("\nEnter the PDF path: ").strip().strip('"')

    if not pdf_path:
        print("Error: PDF path cannot be empty.")
        return

    path = Path(pdf_path)

    if not path.is_file() or path.suffix.lower() != ".pdf":
        print("Error: Please provide a valid PDF file path.")
        return

    document_name = path.name

    try:
        print("\n[1/4] Extracting PDF content...")
        pages, table_records = load_pdf(str(path))

        print("[2/4] Creating text chunks...")
        chunks = chunk_pages(pages)

        # Include extracted tables as searchable chunks.
        for index, table in enumerate(table_records):
            table_text = table.get("text", "").strip()

            if table_text:
                chunks.append({
                    "chunk_id": (
                        f"page_{table['page']}_table_{index}"
                    ),
                    "page": table["page"],
                    "text": table_text
                })

        if not chunks:
            print("Error: No extractable text or tables found.")
            return

        print("[3/4] Generating embeddings...")
        embedded_chunks = embed_chunks(chunks, document_name)

        if not embedded_chunks:
            print("Error: No embeddings were generated.")
            return

        print("[4/4] Storing chunks in ChromaDB...")
        add_chunks(embedded_chunks)

        print("\nDocument ingested successfully.")
        print(f"Document: {document_name}")
        print(f"Chunks processed: {len(embedded_chunks)}")
        print(f"Total records in ChromaDB: {get_count()}")

    except Exception as error:
        print(f"\nIngestion failed: {error}")


def answer_question():
    """Retrieve relevant context and generate an answer."""

    question = input("\nEnter your question: ").strip()

    if not question:
        print("Error: Question cannot be empty.")
        return

    try:
        print("\nSearching the document collection...")
        retrieved_chunks = retrieve(question)

        if not retrieved_chunks:
            print(
                "\nOMNISCIA: The information is not available "
                "in the provided documents."
            )
            return

        print(f"Retrieved {len(retrieved_chunks)} relevant chunks.")

        print("Reranking retrieved chunks...")
        ranked_chunks = rerank(question, retrieved_chunks)

        if not ranked_chunks:
            print(
                "\nOMNISCIA: The information is not available "
                "in the provided documents."
            )
            return

        print("Generating answer...")
        answer = generate_answer(question, ranked_chunks)

        if answer and answer.strip():
            print(f"\nOMNISCIA: {answer.strip()}")
        else:
            print("Error: The model returned an empty answer.")

    except Exception as error:
        print(f"\nQuestion answering failed: {error}")


def main():
    """Run the OMNISCIA command-line application."""

    print("\n" + "=" * 40)
    print("             OMNISCIA")
    print("   Multimodal Document Intelligence")
    print("=" * 40)

    while True:
        print("\n1. Ingest a PDF document")
        print("2. Ask a question")
        print("3. Exit")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            ingest_document()

        elif choice == "2":
            answer_question()

        elif choice == "3":
            print("\nThank you for using OMNISCIA.")
            break

        else:
            print("Invalid option. Please choose 1, 2, or 3.")


if __name__ == "__main__":
    main()
