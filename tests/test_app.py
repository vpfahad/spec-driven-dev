from io import BytesIO

from fastapi.testclient import TestClient
from reportlab.pdfgen import canvas

from ragagentbot.app import app
from ragagentbot.preprocessing import PreprocessingConfig, clean_text, chunk_text, process_pdf_document


client = TestClient(app)


def create_pdf_bytes(text: str) -> bytes:
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.drawString(72, 720, text)
    pdf.save()
    return buffer.getvalue()


def create_multipage_pdf_bytes(page_texts: list[str]) -> bytes:
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    for page_text in page_texts:
        pdf.drawString(72, 720, page_text)
        pdf.showPage()
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
    assert payload["chunk_count"] >= 1
    assert payload["page_count"] == 1


def test_upload_pdf_endpoint_rejects_non_pdf_files():
    response = client.post(
        "/api/v1/documents/upload",
        files={"file": ("notes.txt", b"not a pdf", "text/plain")},
    )

    assert response.status_code == 400
    assert "PDF" in response.json()["detail"]


def test_upload_pdf_endpoint_rejects_unreadable_pdf_bytes():
    response = client.post(
        "/api/v1/documents/upload",
        files={"file": ("broken.pdf", b"not really a pdf", "application/pdf")},
    )

    assert response.status_code == 400
    assert "valid PDF" in response.json()["detail"]


def test_upload_pdf_endpoint_supports_configurable_chunking():
    long_text = " ".join(["chunking"] * 300)
    pdf_bytes = create_pdf_bytes(long_text)

    response = client.post(
        "/api/v1/documents/upload",
        files={"file": ("long.pdf", pdf_bytes, "application/pdf")},
        data={"chunk_size": "200", "chunk_overlap": "40"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["chunk_count"] > 1
    assert payload["preprocessing"] == {"chunk_size": 200, "chunk_overlap": 40}
    assert payload["chunks_preview"][0]["page_number"] == 1


def test_upload_pdf_endpoint_rejects_invalid_chunk_configuration():
    pdf_bytes = create_pdf_bytes("valid text")

    response = client.post(
        "/api/v1/documents/upload",
        files={"file": ("invalid-config.pdf", pdf_bytes, "application/pdf")},
        data={"chunk_size": "100", "chunk_overlap": "100"},
    )

    assert response.status_code == 400
    assert "chunk_overlap" in response.json()["detail"]


def test_clean_text_normalizes_whitespace_and_newlines():
    dirty_text = "Hello\u200b   world\r\n\r\n\r\nThis\t is   a   test"

    assert clean_text(dirty_text) == "Hello world\n\nThis is a test"


def test_chunk_text_maintains_overlap_between_chunks():
    text = " ".join(["word"] * 100)

    chunks = chunk_text(text, chunk_size=120, chunk_overlap=20)

    assert len(chunks) > 1
    for idx in range(1, len(chunks)):
        prev_end = int(chunks[idx - 1]["end_char"])
        current_start = int(chunks[idx]["start_char"])
        assert current_start < prev_end


def test_process_pdf_document_preserves_page_metadata():
    pdf_bytes = create_multipage_pdf_bytes(["First page content", "Second page content"])

    result = process_pdf_document(pdf_bytes, config=PreprocessingConfig(chunk_size=200, chunk_overlap=20))

    assert result["page_count"] == 2
    assert result["chunk_count"] >= 2
    page_numbers = {chunk["page_number"] for chunk in result["chunks"]}
    assert page_numbers == {1, 2}
