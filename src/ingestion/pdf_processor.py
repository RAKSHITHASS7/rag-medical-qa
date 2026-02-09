"""PDF document processor for extracting text and metadata."""

import logging
from pathlib import Path
from typing import List, Dict, Optional
import PyPDF2
from pypdf import PdfReader

logger = logging.getLogger(__name__)


class PDFProcessor:
    """Processes PDF files and extracts text with page-level metadata."""
    
    def __init__(self):
        """Initialize the PDF processor."""
        self.supported_formats = ['.pdf']
    
    def process_pdf(self, pdf_path: str) -> List[Dict[str, any]]:
        """
        Extract text from PDF with page-level metadata.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            List of dictionaries containing page text and metadata
        """
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        if pdf_path.suffix.lower() not in self.supported_formats:
            raise ValueError(f"Unsupported file format: {pdf_path.suffix}")
        
        pages = []
        try:
            reader = PdfReader(str(pdf_path))
            total_pages = len(reader.pages)
            
            logger.info(f"Processing PDF: {pdf_path.name} ({total_pages} pages)")
            
            for page_num, page in enumerate(reader.pages, start=1):
                try:
                    text = page.extract_text()
                    if text.strip():
                        pages.append({
                            'text': text.strip(),
                            'page_number': page_num,
                            'source': pdf_path.name,
                            'total_pages': total_pages
                        })
                except Exception as e:
                    logger.warning(f"Error extracting text from page {page_num}: {e}")
                    continue
            
            logger.info(f"Successfully processed {len(pages)} pages from {pdf_path.name}")
            return pages
            
        except Exception as e:
            logger.error(f"Error processing PDF {pdf_path}: {e}")
            raise
    
    def process_directory(self, directory_path: str) -> List[Dict[str, any]]:
        """
        Process all PDF files in a directory.
        
        Args:
            directory_path: Path to directory containing PDF files
            
        Returns:
            List of all pages from all PDFs
        """
        directory = Path(directory_path)
        if not directory.exists():
            raise FileNotFoundError(f"Directory not found: {directory}")
        
        all_pages = []
        pdf_files = list(directory.glob("*.pdf"))
        
        if not pdf_files:
            logger.warning(f"No PDF files found in {directory}")
            return all_pages
        
        logger.info(f"Found {len(pdf_files)} PDF files in {directory}")
        
        for pdf_file in pdf_files:
            try:
                pages = self.process_pdf(str(pdf_file))
                all_pages.extend(pages)
            except Exception as e:
                logger.error(f"Failed to process {pdf_file}: {e}")
                continue
        
        return all_pages

