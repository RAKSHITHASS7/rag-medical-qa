"""Main RAG pipeline orchestrator."""

import logging
from typing import Optional, Dict, List
from pathlib import Path

from .ingestion import PDFProcessor, DocumentChunker
from .embeddings import Embedder, VectorIndexer
from .retrieval import Retriever
from .generation import AnswerGenerator

logger = logging.getLogger(__name__)


class RAGPipeline:
    """Orchestrates the complete RAG pipeline from ingestion to generation."""
    
    def __init__(
        self,
        model_path: str,
        index_path: Optional[str] = None,
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        retrieval_k: int = 5
    ):
        """
        Initialize the RAG pipeline.
        
        Args:
            model_path: Path to Llama-3 GGUF model
            index_path: Path to save/load FAISS index
            embedding_model: HuggingFace embedding model name
            chunk_size: Document chunk size
            chunk_overlap: Chunk overlap size
            retrieval_k: Number of documents to retrieve
        """
        self.model_path = model_path
        self.index_path = index_path or "models/faiss_index"
        
        # Initialize components
        self.pdf_processor = PDFProcessor()
        self.chunker = DocumentChunker(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        self.embedder = Embedder(model_name=embedding_model)
        self.indexer = VectorIndexer(
            embeddings=self.embedder.embeddings,
            index_path=self.index_path
        )
        self.retriever: Optional[Retriever] = None
        # Initialize generator lazily - don't fail if llama-cpp-python not installed
        # Generator is only needed for querying, not ingestion
        self.generator = None
        self._generator_initialized = False
        self._model_path = model_path  # Store for lazy initialization
        
        logger.info("RAG Pipeline initialized")
    
    def ingest_documents(self, pdf_path: str) -> None:
        """
        Ingest PDF documents and create vector index.
        
        Args:
            pdf_path: Path to PDF file or directory
        """
        logger.info(f"Ingesting documents from: {pdf_path}")
        
        # Process PDFs
        pdf_path_obj = Path(pdf_path)
        if pdf_path_obj.is_file():
            pages = self.pdf_processor.process_pdf(pdf_path)
        elif pdf_path_obj.is_dir():
            pages = self.pdf_processor.process_directory(pdf_path)
        else:
            raise ValueError(f"Invalid path: {pdf_path}")
        
        if not pages:
            raise ValueError("No pages extracted from PDF(s)")
        
        # Chunk documents
        documents = self.chunker.chunk_pages(pages)
        
        # Create index
        self.indexer.create_index(documents)
        self.indexer.save_index()
        
        # Initialize retriever
        self.retriever = Retriever(
            vectorstore=self.indexer.get_vectorstore(),
            k=5
        )
        
        logger.info("Document ingestion completed")
    
    def load_index(self) -> None:
        """Load existing vector index."""
        logger.info(f"Loading index from: {self.index_path}")
        self.indexer.load_index()
        self.retriever = Retriever(
            vectorstore=self.indexer.get_vectorstore(),
            k=5
        )
        logger.info("Index loaded successfully")
    
    def query(self, question: str, k: Optional[int] = None) -> Dict:
        """
        Query the RAG system with a question.
        
        Args:
            question: User question
            k: Optional number of documents to retrieve
            
        Returns:
            Dictionary with answer, citations, and metadata
        """
        if self.retriever is None:
            raise ValueError("No index loaded. Please ingest documents or load index first.")
        
        # Retrieve relevant documents
        documents = self.retriever.retrieve(question, k=k)
        
        if not documents:
            return {
                'answer': "I could not find any relevant information to answer this question.",
                'citations': [],
                'question': question,
                'context_length': 0
            }
        
        # Format context
        context = self.retriever.format_context(documents)
        citations = self.retriever.get_citations(documents)
        
        # Initialize generator if not already done (use demo mode if LLM not available)
        if not self._generator_initialized:
            try:
                self.generator = AnswerGenerator(model_path=self._model_path)
                self._generator_initialized = True
            except Exception as e:
                logger.warning(f"Could not initialize generator: {e}. Using demo mode.")
                self.generator = AnswerGenerator(model_path=self._model_path)
                self._generator_initialized = True
        
        # Generate answer (will use demo mode if LLM not available)
        use_demo = not Path(self._model_path).exists()  # Use demo if model not found
        response = self.generator.generate(
            question=question,
            context=context,
            citations=citations,
            use_demo_mode=use_demo
        )
        
        return response

