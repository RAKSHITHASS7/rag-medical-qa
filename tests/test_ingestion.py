"""Tests for ingestion module."""

import pytest
from pathlib import Path
from src.ingestion import PDFProcessor, DocumentChunker


def test_pdf_processor_initialization():
    """Test PDF processor initialization."""
    processor = PDFProcessor()
    assert processor is not None
    assert '.pdf' in processor.supported_formats


def test_document_chunker_initialization():
    """Test document chunker initialization."""
    chunker = DocumentChunker(chunk_size=1000, chunk_overlap=200)
    assert chunker.chunk_size == 1000
    assert chunker.chunk_overlap == 200


# Add more tests as needed

