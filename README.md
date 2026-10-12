# OMNISCIA — Multimodal Document Intelligence

**An AI-powered document question-answering system built with Retrieval-Augmented Generation (RAG).**

OMNISCIA enables users to ask natural-language questions about their documents and receive answers grounded in retrieved document content. It combines semantic search, cross-encoder reranking, and a locally running Gemma language model to improve the relevance and reliability of generated answers.

## Key Features

- **PDF Processing:** Extracts document text using PyMuPDF.
- **Text Chunking:** Splits documents into smaller chunks for efficient retrieval, with configurable chunk size and overlap.
- **Semantic Embeddings:** Converts text into vector representations using Sentence Transformers.
- **Vector Storage:** Stores document chunks, embeddings, and metadata persistently in ChromaDB.
- **Semantic Retrieval:** Retrieves relevant document chunks based on query similarity.
- **Cross-Encoder Reranking:** Reorders retrieved chunks using a pretrained cross-encoder.
- **Context-Grounded Generation:** Uses Gemma through Ollama to generate answers based on retrieved context.
- **Relevance Filtering:** Rejects retrieved chunks that exceed a configured distance threshold.
- **Error Handling:** Handles invalid PDF inputs, empty inputs, retrieval failures, and missing information.
- **Duplicate-Ingestion Handling:** Uses stable chunk IDs and ChromaDB upserts to avoid duplicate records when the same document is ingested repeatedly under the same conditions.
- **Image Processing Components:** Includes image extraction and vision-analysis components for multimodal document processing.

## Technology Stack

| Component | Technology | Purpose |
|---|---|---|
| Programming language | Python | Application logic |
| PDF processing | PyMuPDF | Extracting document content |
| Embedding model | `all-MiniLM-L6-v2` | Generating semantic embeddings |
| Vector database | ChromaDB | Persistent storage and similarity search |
| Reranking model | `cross-encoder/ms-marco-MiniLM-L-6-v2` | Ranking retrieved passages |
| Language model | Gemma | Answer generation |
| Local model runtime | Ollama | Running the language model locally |
| Testing | pytest | Automated testing |

## Architecture

OMNISCIA follows a Retrieval-Augmented Generation pipeline.

```text
                 PDF Documents
                       |
                       v
              PDF Text Extraction
                       |
                       v
                Text Chunking
                       |
                       v
             Embedding Generation
                       |
                       v
                ChromaDB Storage
                       |
                       v
               User's Question
                       |
                       v
                Query Embedding
                       |
                       v
                Semantic Search
                       |
                       v
              Distance Filtering
                       |
                       v
              Cross-Encoder Reranking
                       |
                       v
             Context + User Question
                       |
                       v
              Gemma via Ollama
                       |
                       v
                 Final Answer
```

The image extraction and vision-analysis components support additional document processing. Their integration into the complete question-answering pipeline depends on the configured ingestion workflow.

## How It Works

### 1. Document Ingestion

The PDF loader extracts text and available table information from a PDF. The extracted content is divided into smaller chunks.

### 2. Embedding Generation

The `all-MiniLM-L6-v2` model converts each chunk into a numerical vector representing its semantic meaning.

### 3. Persistent Storage

OMNISCIA stores chunk text, embeddings, document names, page metadata, and chunk IDs in ChromaDB.

### 4. Semantic Retrieval

A user's question is embedded and compared with stored vectors. The retriever selects candidate chunks and filters out chunks whose distance exceeds the configured threshold.

### 5. Reranking

A cross-encoder evaluates the relationship between the question and each retrieved passage, then ranks the candidates by relevance.

### 6. Answer Generation

The retrieved context and question are passed to Gemma through Ollama. The generation prompt instructs the model to use the supplied evidence, preserve factual details, and identify missing or conflicting information.

### 7. Missing-Information Handling

If retrieval returns no acceptable chunks, OMNISCIA responds:

> The information is not available in the provided documents.

This fallback reduces unsupported responses when relevant evidence cannot be retrieved.

## Installation and Setup

### Prerequisites

- Python 3.11 or another Python version compatible with the project's installed dependencies
- Git
- Ollama
- A Gemma model available through Ollama

### 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd OMNISCIA
```

Replace the placeholder with your actual repository URL.

### 2. Create a Virtual Environment

**Windows PowerShell**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux or macOS**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

Ensure `requirements.txt` lists the dependencies actually used by your project.

### 4. Configure Ollama

Install Ollama from its official website:

https://ollama.com/

Download a compatible Gemma model:

```bash
ollama pull gemma3
```

Start Ollama and confirm that the model is available.

**Note:** The model name in this command is an example. It must match the model name configured in your `LLMClient` implementation.

### 5. Prepare Your Documents

Place the PDF files you want to process in an appropriate local directory, such as:

```text
data/
└── documents/
    └── sample.pdf
```

Ensure your application's configured document paths point to the correct location.

### 6. Run OMNISCIA

From the project root:

```bash
python main.py
```

Use the interactive menu to ingest a PDF and ask questions.

## Example Usage

Suppose a document contains the following data:

| Year | Revenue (USD millions) |
|---|---:|
| 2022 | 20 |
| 2023 | 30 |
| 2024 | 42 |
| 2025 | 55 |

Example questions:

**Question:** What was Asterion Technologies' revenue in 2024?

**Answer:** Approximately 42 million USD.

**Question:** How much did revenue increase from 2022 to 2024?

**Answer:** Revenue increased by approximately 22 million USD.

**Question:** What is the capital of Japan?

**Expected behavior:** OMNISCIA should report that the information is unavailable when no relevant supporting context is retrieved.

These examples illustrate tested behavior with the sample document; results depend on the documents ingested and the retrieval pipeline.

## Testing

Run the automated test suite from the project root:

```bash
python -m pytest -v
```

The current test suite has passed the following checks:

- PDF error handling for missing and empty documents
- Image extraction
- Retrieval of relevant questions
- Rejection of irrelevant questions
- Empty-input handling in embedding generation
- Duplicate-ingestion behavior for repeated processing of the same document

Additional manual checks have exercised numerical question answering, calculations from retrieved facts, and responses to contradictory context.

Passing these tests does not guarantee that all possible questions, documents, or model outputs will be correct.

## Project Structure

The following is a representative structure. Keep the actual filenames and directories consistent with the repository.

```text
OMNISCIA/
├── ingestion/
│   └── pdf_loader.py
├── chunking/
│   └── text_chunking.py
├── embeddings/
│   └── embedder.py
├── storage/
│   └── chroma_store.py
├── retrieval/
│   └── retriever.py
├── reranking/
│   └── reranker.py
├── generation/
│   └── llm_client.py
├── data/
│   └── documents/
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

Add the actual image-processing, vision-analysis, evaluation, and test modules to this tree as they exist in your repository.

## Limitations

- Answer quality depends on document quality, chunking, retrieval, and model behavior.
- The retrieval distance threshold is configurable and may require evaluation on a broader dataset.
- A generated answer can still contain errors even when the prompt instructs the model to use only the supplied context.
- Contradiction handling and numerical reasoning require further systematic evaluation.
- Image extraction and vision analysis do not automatically guarantee complete understanding of every chart, diagram, or scanned page.
- Local model performance depends on available hardware and model configuration.

## Future Improvements

Potential future work includes:

- More comprehensive retrieval evaluation
- Automated answer-grounding evaluation
- Improved table and chart understanding
- Expanded testing with diverse documents
- Performance optimization for large document collections

These are possible extensions, not claims about currently implemented features.

## License

Choose a license before publishing the repository. If you intend to make the project open source, consider adding an appropriate `LICENSE` file.

---

**OMNISCIA** — making document knowledge easier to search, understand, and use.
