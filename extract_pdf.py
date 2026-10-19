"""Extract embedded text from one PDF and return a JSON result on stdout."""

from __future__ import annotations

import json
import os
import sys


MAX_TEXT_CHARS = 50_000


def emit(ok: bool, **values: object) -> None:
    sys.stdout.write(json.dumps({"ok": ok, **values}, ensure_ascii=False))
    sys.stdout.write("\n")


def fail(code: str, message: str, exit_code: int) -> None:
    emit(False, error_code=code, error=message)
    raise SystemExit(exit_code)


def main() -> None:
    if len(sys.argv) != 2:
        fail("invalid_arguments", "A PDF path is required.", 2)

    pdf_path = sys.argv[1]
    if not os.path.isfile(pdf_path):
        fail("invalid_pdf", "The uploaded PDF could not be found.", 3)

    try:
        from pypdf import PdfReader
    except ImportError:
        fail(
            "pypdf_missing",
            "pypdf is not installed for the configured Python interpreter.",
            4,
        )

    try:
        reader = PdfReader(pdf_path, strict=False)
        if reader.is_encrypted:
            fail(
                "encrypted_pdf",
                "Password-protected PDFs are not supported. Remove the password and try again.",
                5,
            )

        parts: list[str] = []
        char_count = 0
        for page in reader.pages:
            text = page.extract_text() or ""
            remaining = MAX_TEXT_CHARS - char_count
            if remaining <= 0:
                break
            parts.append(text[:remaining])
            char_count += min(len(text), remaining)
            if char_count >= MAX_TEXT_CHARS:
                break

        extracted = "\n".join(parts).strip()
    except SystemExit:
        raise
    except Exception:
        fail(
            "invalid_pdf",
            "The PDF could not be parsed. Check that it is a valid, readable PDF.",
            3,
        )

    if not extracted:
        fail(
            "empty_text",
            "No selectable text was found. This may be a scanned PDF; paste the resume text instead.",
            6,
        )

    emit(True, text=extracted)


if __name__ == "__main__":
    main()
