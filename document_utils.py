
import pymupdf # PyMuPDF
import re
from collections import Counter


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract readable text from a PDF file."""
    try:
        with pymupdf.open(stream=file_bytes, filetype="pdf") as pdf:
            text = "\n".join(page.get_text() for page in pdf)
    except Exception as exc:
        raise ValueError("Invalid or unreadable PDF file.") from exc

    if not text.strip():
        raise ValueError(
            "No readable text found in the PDF. "
            "Scanned PDFs may require OCR."
        )

    return text.strip()


def extract_text_from_txt(file_bytes: bytes) -> str:
    """Decode text from a TXT file."""
    try:
        text = file_bytes.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ValueError("The TXT file must use UTF-8 encoding.") from exc

    if not text.strip():
        raise ValueError("The TXT file is empty.")

    return text.strip()


def generate_summary(text: str, max_sentences: int = 3) -> str:
    """Create a simple extractive summary using the first sentences."""
    if not text or not text.strip():
        raise ValueError("Cannot summarize empty text.")

    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    return " ".join(sentences[:max_sentences])


def extract_keywords(text: str, top_n: int = 10) -> list[str]:
    """Extract frequent words, excluding common English words."""
    stop_words = {
        "the", "and", "for", "are", "was", "were", "this",
        "that", "with", "from", "have", "has", "had", "you",
        "your", "not", "but", "can", "will", "its", "into",
        "our", "their", "they", "about", "which", "also",
    }

    words = re.findall(r"\b[a-zA-Z][a-zA-Z-]{2,}\b", text.lower())
    filtered_words = [word for word in words if word not in stop_words]

    return [
        word for word, _ in Counter(filtered_words).most_common(top_n)
    ]
