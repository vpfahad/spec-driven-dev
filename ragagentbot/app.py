from __future__ import annotations

from io import BytesIO
from typing import Any

from fastapi import FastAPI, File, HTTPException, UploadFile
from pypdf import PdfReader

app = FastAPI(title="RAGAgentBot", version="0.1.0")

_DOCUMENTS: dict[str, dict[str, Any]] = {}


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    reader = PdfReader(BytesIO(pdf_bytes))
    text_chunks: list[str] = []

    for page in reader.pages:
        page_text = page.extract_text() or ""
        cleaned = page_text.strip()
        if cleaned:
            text_chunks.append(cleaned)

    return "\n\n".join(text_chunks)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "RAGAgentBot is running.", "status": "ok"}


@app.post("/api/v1/documents/upload")
async def upload_document(file: UploadFile = File(...)) -> dict[str, Any]:
    if file.filename is None or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    pdf_bytes = await file.read()
    if not pdf_bytes:
        raise HTTPException(status_code=400, detail="The uploaded PDF is empty.")

    try:
        text = extract_text_from_pdf(pdf_bytes)
    except Exception as exc:  # pragma: no cover - defensive path for unreadable PDFs
        raise HTTPException(status_code=400, detail="The uploaded file is not a readable PDF.") from exc

    if not text:
        raise HTTPException(status_code=400, detail="The uploaded PDF does not contain readable text.")

    _DOCUMENTS[file.filename] = {
        "filename": file.filename,
        "status": "processed",
        "text": text,
    }

    return {
        "filename": file.filename,
        "status": "processed",
        "text_preview": text[:400],
        "document_id": file.filename,
        "char_count": len(text),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("ragagentbot.app:app", host="127.0.0.1", port=8000, reload=True)
