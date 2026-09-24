# Roadmap

## Guiding Principle
Build the product in very small, testable phases. Each phase should produce a working improvement, provide a clear validation checkpoint, and keep the scope narrow enough to reduce risk.

## Phase 0 — Project Setup and Baseline [Complete]
Goal: establish the repository and initial working environment.

Deliverables:
- Initialize the Python project structure.
- Define the base dependencies.
- Add a minimal README and project conventions.
- Confirm the local environment can run a basic Python app.

Checkpoint:
- The project runs in a clean local environment without blocking setup issues.

Status: Complete — the repository baseline was created and verified with a local smoke test.

---

## Phase 1 — Single PDF Ingestion [Complete]
Goal: create a working upload and extraction flow for one PDF.

Deliverables:
- PDF upload interface or local input path.
- PDF text extraction.
- Simple validation for accepted files.
- Basic handling of malformed or unreadable PDFs.

Checkpoint:
- A PDF can be loaded and its text extracted into a usable form.

Status: Complete — uploaded PDFs are validated, parsed, and their extracted text is returned for use in later retrieval stages.

---

## Phase 2 — Document Preprocessing and Chunking
Goal: convert raw extracted text into searchable chunks.

Deliverables:
- Text cleaning and normalization.
- Chunking strategy for sections, paragraphs, or token windows.
- Metadata tracking for chunk origin and order.

Checkpoint:
- The document is decomposed into meaningful chunks suitable for retrieval.

---

## Phase 3 — Embedding Generation
Goal: produce vector representations for the document and queries.

Deliverables:
- Connect to an Ollama embedding model.
- Create embeddings for document chunks.
- Create embeddings for user questions.
- Validate output shape and consistency.

Checkpoint:
- Chunks and queries can be embedded with the same model configuration.

---

## Phase 4 — FAISS Retrieval
Goal: implement semantic retrieval from the embedded document store.

Deliverables:
- Index the chunk embeddings in FAISS.
- Perform top-k similarity retrieval for a user question.
- Inspect retrieval quality using a few sample questions.

Checkpoint:
- The system retrieves relevant document chunks for test queries.

---

## Phase 5 — Reranking
Goal: improve retrieval quality before answer generation.

Deliverables:
- Add a reranking pass over candidate chunks.
- Prioritize the strongest context for the answer.
- Tune retrieval parameters with a few sample documents.

Checkpoint:
- The top candidate set is meaningfully more relevant than the raw semantic result alone.

---

## Phase 6 — Grounded Answer Generation
Goal: generate answers from document context instead of unsupported general knowledge.

Deliverables:
- Prompt the Ollama chat model with the selected context.
- Include clear instructions for grounding responses in the source document.
- Add a fallback response when the answer is not available in the document.

Checkpoint:
- The model answers from the document context and clearly states when information is missing.

---

## Phase 7 — Conversational Interaction
Goal: support natural follow-up questions and iterative user interaction.

Deliverables:
- Basic chat flow for multiple prompts.
- Maintain the current document context across turns.
- Keep answers grounded in the uploaded document.

Checkpoint:
- A user can ask more than one question about the same PDF in sequence.

---

## Phase 8 — UX and Validation
Goal: make the experience easier to use and more reliable.

Deliverables:
- Simple upload and question interface.
- Status messaging and loading states.
- Basic validation and error handling.
- Minimal end-to-end user testing for realistic questions.

Checkpoint:
- A non-technical user can upload a PDF and ask a question without major friction.

---

## Phase 9 — Hardening and Quality Improvement
Goal: improve answer quality and operational reliability.

Deliverables:
- Retrieval tuning and chunk strategy refinement.
- Prompt improvements for grounded outputs.
- Better handling of edge cases and empty results.
- Documentation for common troubleshooting steps.

Checkpoint:
- The application consistently produces relevant, document-supported answers.

---

## Phase 10 — Future Expansion
Goal: keep the architecture ready for future product growth.

Deliverables:
- Multi-document ingestion path.
- Persistent vector storage options.
- Additional document formats.
- Citation support and richer document metadata.

Checkpoint:
- The foundation is extensible without redesigning the initial architecture.

## Implementation Rule
Do not attempt all phases at once. Each phase should be implemented, tested, and validated before moving to the next one.
