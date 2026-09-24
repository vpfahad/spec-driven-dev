# Phase 0 Plan — Project Setup and Baseline

## Objective
Establish the repository foundation for the RAG application and confirm that a clean local Python environment can run a minimal app without blocking setup issues.

## Task Groups

1. Confirm the Phase 0 scope and acceptance criteria
   - Re-align the work with the roadmap checkpoint for Phase 0.
   - Keep the initial release intentionally narrow and focused on setup, baseline validation, and project conventions.
   - Document the expected outcome before implementation begins.

2. Initialize the project structure
   - Create the top-level project folders and package structure.
   - Add a minimal source layout appropriate for a Python application.
   - Keep the structure simple enough to extend into later phases without rework.

3. Define the base Python environment and dependency set
   - Use uv for dependency and environment management.
   - Add the baseline Python project configuration needed to install dependencies reproducibly.
   - Include the core libraries required for the first working application path, while avoiding unnecessary scope creep.

4. Add the minimal application entry point
   - Create a simple app that can run successfully in a local environment.
   - Keep the behavior intentionally minimal: a working startup path and a basic smoke check.
   - Ensure the app can be executed without requiring the full RAG pipeline to be implemented yet.

5. Add project conventions and onboarding documentation
   - Create a minimal README with local setup steps.
   - Document the expected commands for environment creation and app execution.
   - Record basic conventions for package layout, dependency management, and validation steps.

6. Validate the baselined project locally
   - Install dependencies in a clean environment.
   - Run the minimal application successfully.
   - Check that the project is ready for future phases without setup blockers.
   - Capture any issues that must be fixed before the phase is considered complete.

7. Review and prepare for Phase 1
   - Confirm the repository is stable and ready for the next phase.
   - Ensure the baseline can support PDF ingestion work without requiring a redesign.
   - Document the handoff into the single PDF ingestion phase.
