# Technology Stack

## Recommended Stack for the Initial Release
The project will prioritize a lightweight, local-first Python stack that matches the stakeholder vision and supports fast iteration.

### Core Stack
- Python
- uv for package and environment management
- FastAPI for the API layer
- Pydantic for data validation and models
- LangChain
- FAISS
- Ollama for embeddings
- Ollama for chat / generation model
- PDF parsing library for extraction

### Rationale
This stack aligns with the project goals of:
- running locally without heavy infrastructure
- keeping the implementation understandable for a small team
- focusing on retrieval quality and grounded answer generation
- minimizing dependence on hosted cloud services during early validation
- using a modern, lightweight Python developer workflow with fast API development and strong validation

## Proposed Components

### 1. Application Layer
- Python as the primary application language.
- uv for environment creation, dependency management, and reproducible local setup.
- FastAPI for the service layer and HTTP interface.
- Pydantic models for request/response validation and structured app contracts.
- Small project structure for ingestion, retrieval, and prompting.
- Clear separation between document processing, retrieval, and answer generation.

### 2. Document Processing
- PDF extraction library to read and normalize text from uploaded PDFs.
- Document cleaning and preprocessing for predictable chunking.
- Chunk splitting logic targeted at semantic relevance rather than arbitrary size alone.

### 3. Embedding Layer
- Ollama embedding model for converting document chunks and questions into vector representations.
- A consistent embedding strategy for both document content and user queries.

### 4. Vector Store
- FAISS as the in-memory vector store for initial retrieval.
- Fast nearest-neighbor search for matching relevant chunks.

### 5. Retrieval and Re-ranking
- Initial semantic retrieval from FAISS.
- Candidate reranking step to prioritize the most contextually relevant chunks before generation.

### 6. Generation Layer
- Ollama-hosted chat model to answer questions grounded in retrieved context.
- Prompting strategy that emphasizes using only the document context and acknowledging missing information when needed.

### 7. UI / Interaction Layer
- Keep the first UI lightweight and easy to operate.
- A simple interface for upload, question entry, and answer display.
- The UI can evolve independently from the retrieval architecture.

## Non-Functional Expectations
- Local-first setup for development and testing.
- Simple dependency management.
- No requirement for enterprise-scale persistence in the first release.
- Ability to run with minimal operational complexity.

## Technology Decision Summary
The initial implementation should stay intentionally narrow and practical:

Python + uv + FastAPI + Pydantic + LangChain + Ollama + FAISS + PDF extraction

This is the default architecture for the first working version and offers a strong foundation for future enhancement without overengineering the product at the start.
