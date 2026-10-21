"""
PDF Parsing and Text Extraction Utilities
Author: Dilkhush Raj (https://github.com/Dilkhush144)
"""

import io
import re
from typing import Union
import pdfplumber


def read_pdf(file_source: Union[io.BytesIO, str, object]) -> str:
    """
    Extracts text from a PDF file-like object (Streamlit UploadedFile) or file path.
    """
    extracted_text = []

    try:
        if hasattr(file_source, "seek"):
            file_source.seek(0)

        with pdfplumber.open(file_source) as pdf:
            if not pdf.pages:
                return ""
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    extracted_text.append(text)
    except Exception as e:
        # If extraction fails, raise or return error string
        raise RuntimeError(f"Failed to extract text from PDF: {str(e)}")

    return "\n\n".join(extracted_text)


def clean_text(text: str) -> str:
    """
    Normalizes whitespace, removes unprintable non-ASCII glyphs, and preserves readable words.
    """
    if not text:
        return ""

    # Replace tabs and carriage returns with space
    text = text.replace("\r", " ").replace("\t", " ")

    # Collapse multiple whitespace
    text = re.sub(r"[ \t]+", " ", text)

    # Collapse more than 2 consecutive newlines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()
