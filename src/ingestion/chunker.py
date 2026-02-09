"""Document chunking strategies for RAG."""

import logging
from typing import List, Dict, Optional
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

logger = logging.getLogger(__name__)


class DocumentChunker:
    """Chunks documents with overlap and metadata preservation."""
    
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        separators: Optional[List[str]] = None
    ):
        """
        Initialize the document chunker.
        
        Args:
            chunk_size: Maximum size of each chunk in characters
            chunk_overlap: Overlap between chunks in characters
            separators: List of separators to use for splitting
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        if separators is None:
            separators = ["\n\n", "\n", ". ", " ", ""]
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=separators,
            length_function=len
        )
    
    def chunk_pages(self, pages: List[Dict[str, any]]) -> List[Document]:
        """
        Chunk pages into smaller documents with metadata.
        
        Args:
            pages: List of page dictionaries with 'text', 'page_number', 'source'
            
        Returns:
            List of LangChain Document objects with metadata
        """
        documents = []
        
        for page in pages:
            text = page.get('text', '')
            if not text.strip():
                continue
            
            # Create LangChain Document with metadata
            doc = Document(
                page_content=text,
                metadata={
                    'page_number': page.get('page_number', 0),
                    'source': page.get('source', 'unknown'),
                    'total_pages': page.get('total_pages', 0)
                }
            )
            
            # Split into chunks if needed
            chunks = self.text_splitter.split_documents([doc])
            
            # Add chunk index to metadata
            for idx, chunk in enumerate(chunks):
                chunk.metadata['chunk_index'] = idx
                chunk.metadata['total_chunks'] = len(chunks)
            
            documents.extend(chunks)
        
        logger.info(f"Created {len(documents)} chunks from {len(pages)} pages")
        return documents
    
    def chunk_text(self, text: str, metadata: Optional[Dict] = None) -> List[Document]:
        """
        Chunk a single text string.
        
        Args:
            text: Text to chunk
            metadata: Optional metadata dictionary
            
        Returns:
            List of LangChain Document objects
        """
        if metadata is None:
            metadata = {}
        
        doc = Document(page_content=text, metadata=metadata)
        chunks = self.text_splitter.split_documents([doc])
        
        for idx, chunk in enumerate(chunks):
            chunk.metadata['chunk_index'] = idx
            chunk.metadata['total_chunks'] = len(chunks)
        
        return chunks

