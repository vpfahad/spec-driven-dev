from io import BytesIO

from fastapi.testclient import TestClient
from reportlab.pdfgen import canvas

from ragagentbot.app import app


client = TestClient(app)


def create_pdf_bytes(text: str) -> bytes:
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.drawString(72, 720, text)
    pdf.save()
    return buffer.getvalue()


def test_root_endpoint_returns_status_message():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "RAGAgentBot is running.",
        "status": "ok",
    }


def test_upload_pdf_endpoint_extracts_text():
    pdf_bytes = create_pdf_bytes("Phase 1 PDF ingestion is working.")

    response = client.post(
        "/api/v1/documents/upload",
        files={"file": ("sample.pdf", pdf_bytes, "application/pdf")},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["filename"] == "sample.pdf"
    assert payload["status"] == "processed"
    assert "Phase 1 PDF ingestion is working." in payload["text_preview"]


def test_upload_pdf_endpoint_rejects_non_pdf_files():
    response = client.post(
        "/api/v1/documents/upload",
        files={"file": ("notes.txt", b"not a pdf", "text/plain")},
    )

    assert response.status_code == 400
    assert "PDF" in response.json()["detail"]
