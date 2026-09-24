# Phase 0 Requirements — Project Setup and Baseline

## Scope
This phase is intentionally limited to the repository baseline and local environment readiness required before building the RAG workflow.

The work must include:
- a minimal Python project structure
- baseline dependency management with uv
- basic project configuration for local execution
- a minimal README and setup instructions
- a working local smoke test for the application

The work must not include:
- PDF ingestion logic
- chunking logic
- embedding generation
- FAISS retrieval
- reranking
- answer generation
- UI implementation

## Decision
The project will adopt a minimal but extensible Python foundation that supports the future product architecture without overbuilding the first phase.

Key decisions for this phase:
- Use Python as the application language.
- Use uv to manage the environment and install dependencies.
- Keep the package structure simple and easy to extend.
- Prefer a minimal application entry point that proves the environment works.
- Keep documentation lean and practical for developers.

## Context
This phase is the foundation for the roadmap’s Phase 1 and beyond. The project is expected to move quickly, so the goal is to remove setup friction before adding the actual retrieval and generation layers.

The baseline must be easy to reproduce on a developer machine and should reflect the project’s local-first, lightweight approach described in the mission and technology stack documents.

## Acceptance Criteria
The phase is complete when:
- the repository has a valid Python project structure
- dependencies are installed via uv in a reproducible way
- a minimal app can run successfully in the local environment
- project instructions are clear enough for a developer to set up the app without extra discovery work
- there are no blocking setup issues preventing progress to Phase 1
