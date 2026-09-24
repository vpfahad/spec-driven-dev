from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
import re
import unicodedata

from pypdf import PdfReader


class PreprocessingError(ValueError):
    """Raised when a document cannot be preprocessed safely."""


@dataclass(frozen=True)
class PreprocessingConfig:
    chunk_size: int = 800
    chunk_overlap: int = 120

    def validate(self) -> None:
        if self.chunk_size < 100:
            raise PreprocessingError("chunk_size must be at least 100 characters.")
        if self.chunk_overlap < 0:
            raise PreprocessingError("chunk_overlap must be greater than or equal to 0.")
        if self.chunk_overlap >= self.chunk_size:
            raise PreprocessingError("chunk_overlap must be smaller than chunk_size.")


def _is_pdf_signature(pdf_bytes: bytes) -> bool:
    return pdf_bytes.startswith(b"%PDF")


def _extract_page_texts(reader: PdfReader) -> list[dict[str, int | str]]:
    pages: list[dict[str, int | str]] = []
    for index, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text() or ""
        cleaned = clean_text(page_text)
        if cleaned:
            pages.append(
                {
                    "page_number": index,
                    "text": cleaned,
                }
            )
    return pages


def clean_text(text: str) -> str:
    normalized = unicodedata.normalize("NFKC", text)
    normalized = normalized.replace("\r\n", "\n").replace("\r", "\n")
    normalized = normalized.replace("\u200b", "")
    normalized = re.sub(r"[ \t]+", " ", normalized)
    normalized = re.sub(r"\n{3,}", "\n\n", normalized)
    return normalized.strip()


def chunk_text(text: str, *, chunk_size: int, chunk_overlap: int) -> list[dict[str, int | str]]:
    if not text:
        return []

    if chunk_overlap >= chunk_size:
        raise PreprocessingError("chunk_overlap must be smaller than chunk_size.")

    chunks: list[dict[str, int | str]] = []
    start = 0
    text_length = len(text)

    while start < text_length:
        rough_end = min(start + chunk_size, text_length)
        end = rough_end

        if rough_end < text_length:
            search_floor = start + int(chunk_size * 0.6)
            whitespace_idx = text.rfind(" ", search_floor, rough_end)
            if whitespace_idx > start:
                end = whitespace_idx

        chunk_text_value = text[start:end].strip()
        if chunk_text_value:
            chunks.append(
                {
                    "text": chunk_text_value,
                    "start_char": start,
                    "end_char": end,
                    "char_count": len(chunk_text_value),
                }
            )

        if end >= text_length:
            break

        next_start = max(0, end - chunk_overlap)
        if next_start <= start:
            next_start = start + 1
        start = next_start

    return chunks


def process_pdf_document(
    pdf_bytes: bytes,
    *,
    config: PreprocessingConfig,
) -> dict[str, object]:
    if not pdf_bytes:
        raise PreprocessingError("The uploaded PDF is empty.")
    if not _is_pdf_signature(pdf_bytes):
        raise PreprocessingError("The uploaded file is not a valid PDF.")

    config.validate()

    try:
        reader = PdfReader(BytesIO(pdf_bytes))
    except Exception as exc:  # pragma: no cover - defensive path for broken PDFs
        raise PreprocessingError("The uploaded file is not a readable PDF.") from exc

    pages = _extract_page_texts(reader)
    if not pages:
        raise PreprocessingError("The uploaded PDF does not contain readable text.")

    chunks: list[dict[str, int | str]] = []
    for page in pages:
        page_number = int(page["page_number"])
        page_text = str(page["text"])
        page_chunks = chunk_text(
            page_text,
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
        )
        for chunk_index, chunk in enumerate(page_chunks):
            chunks.append(
                {
                    "chunk_id": f"p{page_number}-c{chunk_index}",
                    "page_number": page_number,
                    "text": chunk["text"],
                    "start_char": chunk["start_char"],
                    "end_char": chunk["end_char"],
                    "char_count": chunk["char_count"],
                }
            )

    all_text = "\n\n".join(str(page["text"]) for page in pages)

    return {
        "text": all_text,
        "pages": pages,
        "chunks": chunks,
        "page_count": len(pages),
        "chunk_count": len(chunks),
        "char_count": len(all_text),
        "preprocessing": {
            "chunk_size": config.chunk_size,
            "chunk_overlap": config.chunk_overlap,
        },
    }
