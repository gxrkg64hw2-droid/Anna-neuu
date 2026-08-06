"""PDF text extraction using PyMuPDF.

License note: PyMuPDF is AGPL. Acceptable for personal academic use.
For commercial reuse, swap to pypdfium2 (BSD) at this interface.
"""
from __future__ import annotations

import re
import re as _re_pdf
from dataclasses import dataclass
from pathlib import Path

import pymupdf


class EncryptedPDFError(RuntimeError):
    """Raised when a PDF is password-protected and cannot be opened."""
    pass


@dataclass(frozen=True)
class Page:
    pdf_page: int          # 1-indexed
    text: str
    word_count: int
    char_count: int


def extract_pages(pdf_path: Path) -> list[Page]:
    """Extract text per page. 1-indexed page numbers.

    Raises EncryptedPDFError if the PDF is password-protected.
    """
    pages: list[Page] = []
    try:
        doc = pymupdf.open(str(pdf_path))
    except Exception as e:
        raise RuntimeError(f"Failed to open PDF {pdf_path.name}: {e}") from e

    if doc.is_encrypted:
        # Try empty password (some PDFs are "encrypted" with no real password)
        try:
            success = doc.authenticate("")
            if not success:
                doc.close()
                raise EncryptedPDFError(
                    f"PDF {pdf_path.name} is password-protected. "
                    f"Use a tool like `qpdf --decrypt` to remove encryption first."
                )
        except EncryptedPDFError:
            raise
        except Exception:
            doc.close()
            raise EncryptedPDFError(
                f"PDF {pdf_path.name} is password-protected. "
                f"Use a tool like `qpdf --decrypt` to remove encryption first."
            )

    try:
        for i, page in enumerate(doc, start=1):
            text = page.get_text("text")
            words = re.findall(r"\b\w+\b", text)
            pages.append(Page(
                pdf_page=i,
                text=text,
                word_count=len(words),
                char_count=len(text),
            ))
    finally:
        doc.close()
    return pages


def extract_title_candidates(pdf_path: Path, top_n: int = 3) -> list[str]:
    """Return up to top_n title candidates from page 1, ranked by font size desc.

    Uses PyMuPDF's structured text extraction. The largest contiguous run of
    text in a single style is treated as the title candidate.
    """
    candidates: list[tuple[float, str]] = []  # (font_size, text)
    with pymupdf.open(str(pdf_path)) as doc:
        if not doc.page_count:
            return []
        page = doc[0]
        d = page.get_text("dict")
        for block in d.get("blocks", []):
            if block.get("type") != 0:  # text blocks only
                continue
            for line in block.get("lines", []):
                # Concatenate spans of the same line into one string
                spans = line.get("spans", [])
                if not spans:
                    continue
                # Use the largest font in this line as its representative
                size = max(s.get("size", 0) for s in spans)
                text = " ".join(s.get("text", "") for s in spans).strip()
                if len(text) >= 6:
                    candidates.append((size, text))
    # Sort by font size desc, then dedupe while preserving order
    candidates.sort(key=lambda x: x[0], reverse=True)
    seen: set[str] = set()
    out: list[str] = []
    for _size, text in candidates:
        if text not in seen:
            seen.add(text)
            out.append(text)
        if len(out) >= top_n:
            break
    return out


_ARXIV_RE = _re_pdf.compile(r"arXiv:(\d{4}\.\d{4,6})", _re_pdf.IGNORECASE)


def extract_arxiv_id(text: str) -> str | None:
    """Find arXiv:XXXX.NNNNN style identifier in text."""
    m = _ARXIV_RE.search(text)
    return m.group(1) if m else None
