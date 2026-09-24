# RAG Application — Stakeholder Vision

## 1. Overview

The objective of this project is to build a **Retrieval-Augmented Generation (RAG) application** that allows users to upload PDF documents and interact with their content using natural language.

The application will enable users to:

* Upload PDF documents.
* Automatically process and understand the uploaded documents.
* Split documents into meaningful chunks.
* Convert document content into vector representations.
* Store the vectors in an in-memory FAISS vector database.
* Ask questions about the uploaded document using natural language.
* Retrieve the most relevant sections of the document.
* Rerank retrieved content to improve the relevance of the information provided to the language model.
* Generate answers using an Ollama-hosted Large Language Model (LLM).
* Use an Ollama embedding model for document and query embeddings.

The overall vision is to provide a **simple document-question-answering experience**, where users can interact with their own PDF content without manually searching through lengthy documents.

---

## 2. Business Vision

Large PDF documents can contain significant amounts of valuable information, but manually locating specific information can be time-consuming.

The proposed RAG application aims to make this information easier to access by allowing users to simply ask questions in natural language.

### Example

Instead of manually searching through a 200-page document for information such as:

> "What are the key recommendations mentioned in the report?"

The user should be able to upload the document and ask the question directly.

The application will identify the most relevant content from the document and use that information to generate a meaningful response.

The intended experience is:

**Upload → Process → Ask → Retrieve → Rerank → Generate Answer**

---

## 3. Project Objectives

The primary objectives of the application are:

1. Provide a simple interface for uploading PDF documents.
2. Automatically process uploaded documents.
3. Make document content searchable using semantic similarity.
4. Enable natural-language conversations with document content.
5. Improve retrieval quality through document reranking.
6. Generate responses grounded in the uploaded documents.
7. Use locally hosted Ollama models for both embeddings and language generation.
8. Provide a lightweight and easy-to-use RAG solution.
9. Keep the initial solution focused on PDF-based document interaction.
10. Establish a foundation that can be extended with additional capabilities in the future.

---

## 4. Scope

### In Scope

The initial version of the application will support:

* PDF document upload.
* PDF text extraction.
* Document preprocessing.
* Document chunking.
* Embedding generation.
* FAISS vector storage.
* Semantic document retrieval.
* Retrieval reranking.
* Natural-language question answering.
* Conversational interaction with uploaded documents.
* Ollama-based embedding models.
* Ollama-based chat/LLM models.
* Python-based application development.
* LangChain-based RAG orchestration.

### Out of Scope for the Initial Version

The initial solution is intentionally focused on PDF documents.

The following capabilities are not part of the initial vision unless introduced as future enhancements:

* Word documents.
* Excel files.
* PowerPoint files.
* Images as standalone documents.
* Audio or video files.
* Enterprise document-management integrations.
* Large-scale distributed vector databases.
* Multi-user enterprise access management.
* Production-grade document persistence across independent application deployments.

These capabilities may be considered in future phases based on stakeholder requirements.

---

# 5. Expected User Journey

The application should provide a straightforward user experience.

## Step 1 — Upload PDF

The user selects and uploads a PDF document.

Example:

```text
User
  |
  | Upload PDF
  v
RAG Application
```

The application validates and accepts the PDF for processing.

---

## Step 2 — Document Processing

After upload, the application processes the document.

The document content is extracted and divided into smaller, meaningful sections or **chunks**.

Chunking is important because large documents cannot be efficiently provided to the language model as a single piece of content.

Conceptually:

```text
PDF Document
      |
      v
Text Extraction
      |
      v
Document Cleaning / Processing
      |
      v
Document Chunking
      |
      +---- Chunk 1
      +---- Chunk 2
      +---- Chunk 3
      +---- ...
      +---- Chunk N
```

---

## Step 3 — Generate Embeddings

Each document chunk is converted into a numerical representation called an **embedding**.

The embedding captures the semantic meaning of the content and allows the system to identify content that is conceptually related to a user's question.

The application will use an **Ollama embedding model** for this purpose.

Conceptually:

```text
Document Chunk
      |
      v
Ollama Embedding Model
      |
      v
Vector Representation
```

---

## Step 4 — Store in FAISS

The generated embeddings will be stored in a **FAISS vector database**.

FAISS will allow the application to efficiently search for document chunks that are semantically relevant to a user's question.

The intended initial solution uses FAISS as an in-memory vector store.

Conceptually:

```text
Document Chunks
      |
      v
Embeddings
      |
      v
FAISS Vector Store
```

---

# 6. Question Answering Experience

Once a document has been processed, the user can ask questions about its content.

For example:

```text
User:
"What are the main risks identified in the document?"
```

The application will process the question and convert it into an embedding using the same embedding approach used for the document.

The system will then search the FAISS vector store to identify relevant document sections.

---

# 7. Retrieval and Reranking

Retrieval is a critical part of the RAG application.

The system will initially retrieve a set of potentially relevant document chunks from FAISS.

However, semantic similarity alone may not always identify the best possible context.

Therefore, the application will include a **reranking stage**.

### Conceptual flow

```text
User Question
      |
      v
Question Embedding
      |
      v
FAISS Retrieval
      |
      v
Candidate Document Chunks
      |
      v
Reranking
      |
      v
Most Relevant Context
      |
      v
Ollama LLM
      |
      v
Generated Answer
```

Reranking is intended to improve the quality of the context provided to the language model by prioritizing the most relevant retrieved content.

This should help reduce situations where less-relevant document sections are given higher priority simply because they have a similar semantic representation.

---

# 8. Current API Baseline

The current baseline exposes a FastAPI service with a PDF upload endpoint:

- `POST /api/v1/documents/upload`

Form fields:

- `file` (required): PDF file upload
- `chunk_size` (optional, default `800`): max characters per chunk, minimum `100`
- `chunk_overlap` (optional, default `120`): overlap between adjacent chunks, must be `< chunk_size`

Behavior:

- Rejects non-PDF files and unreadable/corrupted PDFs with clear error messages.
- Extracts text page-by-page.
- Normalizes text (encoding + whitespace cleanup).
- Chunks text with overlap while preserving per-page metadata.

# 8. Answer Generation

After the relevant document content has been retrieved and reranked, the selected context will be provided to an Ollama-hosted language model.

The LLM will use:

* The user's question.
* The retrieved document context.
* Appropriate instructions for answering based on the available context.

The model will then generate the final response.

Conceptually:

```text
User Question
      +
Relevant Document Context
      |
      v
Ollama Chat Model
      |
      v
Natural Language Answer
```

The goal is for the generated answer to be **grounded in the uploaded document**, rather than relying solely on the model's general knowledge.

---

# 9. Conversational Interaction

The application should allow users to interact with the uploaded document using natural language.

Example conversation:

```text
User:
What is the purpose of this report?

Assistant:
The report describes ...

User:
What are the major risks mentioned?

Assistant:
The document identifies the following major risks ...

User:
Which one is considered the most significant?

Assistant:
Based on the relevant sections of the document ...
```

The intended experience is similar to having a conversation with the document rather than performing traditional keyword-based document searches.

---

# 10. Technology Vision

The solution will use a lightweight Python-based RAG architecture.

The key technologies are:

| Area                     | Technology / Approach        |
| ------------------------ | ---------------------------- |
| Application Language     | Python                       |
| RAG Orchestration        | LangChain                    |
| Document Type            | PDF                          |
| Vector Store             | FAISS                        |
| Embedding Model          | Ollama                       |
| Chat / Generation Model  | Ollama                       |
| Retrieval                | Semantic Vector Search       |
| Retrieval Improvement    | Reranking                    |
| Application Architecture | RAG-based Question Answering |

These technologies represent the **solution direction** rather than a detailed technical implementation specification.

---

# 11. High-Level Solution Architecture

The overall vision can be represented as follows:

```text
                         ┌──────────────────────┐
                         │        User          │
                         └──────────┬───────────┘
                                    │
                         Upload PDF / Ask Question
                                    │
                                    v
                    ┌──────────────────────────────┐
                    │       RAG Application        │
                    │            Python            │
                    │          LangChain           │
                    └──────────────┬───────────────┘
                                   │
                 ┌─────────────────┴─────────────────┐
                 │                                   │
                 v                                   v
        ┌─────────────────┐                 ┌─────────────────┐
        │  PDF Processing │                 │ User Question   │
        └────────┬────────┘                 └────────┬────────┘
                 │                                   │
                 v                                   v
        ┌─────────────────┐                 ┌─────────────────┐
        │ Document Chunks │                 │ Query Embedding │
        └────────┬────────┘                 └────────┬────────┘
                 │                                   │
                 v                                   │
        ┌─────────────────┐                           │
        │ Ollama Embedding│                           │
        │      Model      │                           │
        └────────┬────────┘                           │
                 │                                   │
                 v                                   v
             ┌──────────────────────────────────────────┐
             │              FAISS Vector Store         │
             └────────────────────┬─────────────────────┘
                                  │
                                  v
                         ┌─────────────────┐
                         │    Retrieval    │
                         └────────┬────────┘
                                  │
                                  v
                         ┌─────────────────┐
                         │    Reranking    │
                         └────────┬────────┘
                                  │
                                  v
                         ┌─────────────────┐
                         │ Relevant Context│
                         └────────┬────────┘
                                  │
                                  v
                         ┌─────────────────┐
                         │ Ollama Chat LLM │
                         └────────┬────────┘
                                  │
                                  v
                         ┌─────────────────┐
                         │  Final Answer   │
                         └─────────────────┘
```

---

# 12. Grounded Responses

A key expectation of the application is that answers should be based primarily on the content retrieved from the uploaded document.

The application should avoid presenting unsupported information as if it came from the document.

When relevant information cannot be found in the uploaded document, the desired behavior is for the application to clearly indicate that the information is not available in the provided document rather than unnecessarily generating an unsupported answer.

This is an important aspect of building user trust in the application.

---

# 13. Document Context

The quality of the final response will depend significantly on the quality of the retrieved document context.

The solution therefore considers the following stages as important:

```text
PDF
 ↓
Text Extraction
 ↓
Chunking
 ↓
Embedding
 ↓
Vector Storage
 ↓
Semantic Retrieval
 ↓
Reranking
 ↓
Context Selection
 ↓
LLM Response
```

Each stage contributes to the overall quality of the RAG experience.

---

# 14. Expected Benefits

The proposed application is expected to provide the following benefits:

### Faster Information Discovery

Users can find relevant information without manually reading an entire document.

### Natural-Language Interaction

Users can ask questions in ordinary language instead of learning a specific search syntax.

### Improved Retrieval

Reranking provides an additional mechanism for selecting the most relevant content before answer generation.

### Document-Centric Answers

The system is designed to use the uploaded document as the primary source of context.

### Lightweight Solution

FAISS and locally hosted Ollama models provide a relatively lightweight approach for the initial solution.

### Flexible Foundation

The RAG architecture provides a foundation that can be expanded with additional document types, models, storage options, and enterprise capabilities in future phases.

---

# 15. Initial User Experience

The initial user experience should remain simple.

A typical interaction should look like:

```text
┌────────────────────────────────────────────┐
│              RAG Application               │
├────────────────────────────────────────────┤
│                                            │
│  Upload your PDF                           │
│                                            │
│  [ Choose PDF ]                            │
│                                            │
│  Document: Annual_Report.pdf               │
│  Status: Ready                             │
│                                            │
├────────────────────────────────────────────┤
│                                            │
│  Ask a question about the document         │
│                                            │
│  [ What are the key findings?          ]   │
│                                            │
│                 [ Ask ]                    │
│                                            │
├────────────────────────────────────────────┤
│                                            │
│  Answer                                    │
│                                            │
│  The document identifies ...               │
│                                            │
└────────────────────────────────────────────┘
```

The final UI design can evolve independently from the core RAG vision.

---

# 16. Quality Expectations

The solution should aim to provide:

* Relevant answers.
* Responses grounded in the uploaded document.
* Good retrieval accuracy.
* Meaningful document chunking.
* Effective semantic search.
* Improved context selection through reranking.
* Clear responses when information is unavailable.
* Reasonable response times.
* A simple and intuitive user experience.

The quality of the system should be evaluated not only based on whether an answer is generated, but also on whether the answer is **relevant, accurate, and supported by the available document context**.

---

# 17. Future Enhancement Opportunities

The initial PDF-focused solution can provide a foundation for future capabilities.

Potential future enhancements include:

### Additional Document Types

Support for:

* DOCX
* PPTX
* XLSX
* TXT
* HTML
* Images and scanned documents

### Improved Document Understanding

Future versions could support:

* Tables.
* Images.
* Charts.
* Structured data.
* OCR for scanned PDFs.
* More advanced document layout understanding.

### Persistent Document Storage

The initial solution uses an in-memory FAISS approach. Future versions could consider persistent or enterprise-grade vector storage depending on scale and operational requirements.

### Multi-Document Question Answering

Users could eventually upload multiple documents and ask questions across the entire document collection.

### Document Collections

Documents could be organized into logical collections or knowledge bases.

For example:

```text
Knowledge Base
 ├── Financial Reports
 ├── Project Documents
 ├── Policies
 └── Technical Documentation
```

### Advanced Citations

Future versions could provide references to:

* Document name.
* Page number.
* Relevant section.
* Retrieved passage.

This would make it easier for users to verify generated responses.

### Enterprise Integration

Future phases could potentially integrate with enterprise repositories and document-management platforms.

---

# 18. Success Criteria

The initial solution should be considered successful when a user can:

1. Upload a PDF successfully.
2. Have the document automatically processed.
3. Have document content converted into searchable representations.
4. Ask a natural-language question.
5. Retrieve relevant information from the uploaded document.
6. Have retrieved content reranked for relevance.
7. Receive a meaningful answer generated using the relevant document context.
8. Continue asking follow-up questions about the document.
9. Receive an appropriate response when the requested information is not available.

The primary measure of success is therefore the **quality and usefulness of the document-question-answering experience**, rather than the complexity of the underlying implementation.

---

# 19. Project Vision Summary

The project aims to deliver a simple but effective **PDF-based Retrieval-Augmented Generation application**.

At a high level:

```text
                    PDF DOCUMENT
                         │
                         ▼
                    PROCESSING
                         │
                         ▼
                      CHUNKS
                         │
                         ▼
                 OLLAMA EMBEDDINGS
                         │
                         ▼
                  FAISS VECTOR DB
                         │
                         │
                    USER QUESTION
                         │
                         ▼
                     RETRIEVAL
                         │
                         ▼
                     RERANKING
                         │
                         ▼
                 RELEVANT CONTEXT
                         │
                         ▼
                  OLLAMA CHAT LLM
                         │
                         ▼
                  GROUNDED ANSWER
```

The overall vision is to transform static PDF documents into an **interactive knowledge source** that users can query using natural language.

The initial solution will intentionally remain focused on the core RAG experience:

**Upload a PDF → Understand the document → Ask questions → Retrieve relevant information → Rerank the context → Generate a grounded answer.**

This provides a clear foundation for future expansion into a broader enterprise document intelligence and knowledge platform.
