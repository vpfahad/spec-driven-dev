from __future__ import annotations

from typing import Any

from fastapi import FastAPI, File, Form, HTTPException, UploadFile

from ragagentbot.preprocessing import PreprocessingConfig, PreprocessingError, process_pdf_document

app = FastAPI(title="RAGAgentBot", version="0.1.0")

_DOCUMENTS: dict[str, dict[str, Any]] = {}


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """Backward-compatible helper used by earlier tests and phase code."""
    result = process_pdf_document(pdf_bytes, config=PreprocessingConfig())
    return str(result["text"])


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "RAGAgentBot is running.", "status": "ok"}


@app.post("/api/v1/documents/upload")
async def upload_document(
    file: UploadFile = File(...),
    chunk_size: int = Form(800),
    chunk_overlap: int = Form(120),
) -> dict[str, Any]:
    if file.filename is None or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    pdf_bytes = await file.read()

    try:
        config = PreprocessingConfig(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        result = process_pdf_document(pdf_bytes, config=config)
    except PreprocessingError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    _DOCUMENTS[file.filename] = {
        "filename": file.filename,
        "status": "processed",
        "text": result["text"],
        "chunks": result["chunks"],
        "pages": result["pages"],
        "preprocessing": result["preprocessing"],
    }

    return {
        "filename": file.filename,
        "status": "processed",
        "text_preview": str(result["text"])[:400],
        "document_id": file.filename,
        "char_count": result["char_count"],
        "page_count": result["page_count"],
        "chunk_count": result["chunk_count"],
        "chunks_preview": result["chunks"][:3],
        "preprocessing": result["preprocessing"],
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("ragagentbot.app:app", host="127.0.0.1", port=8000, reload=True)
