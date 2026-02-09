"""Text embedding generation for semantic search."""

import logging
from typing import List, Optional
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document

logger = logging.getLogger(__name__)


class Embedder:
    """Generates embeddings for documents using HuggingFace models."""
    
    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs: Optional[dict] = None,
        encode_kwargs: Optional[dict] = None
    ):
        """
        Initialize the embedder.
        
        Args:
            model_name: HuggingFace model name for embeddings
            model_kwargs: Additional model arguments
            encode_kwargs: Additional encoding arguments
        """
        if model_kwargs is None:
            model_kwargs = {"device": "cpu"}
        
        if encode_kwargs is None:
            encode_kwargs = {"normalize_embeddings": True}
        
        logger.info(f"Initializing embedder with model: {model_name}")
        self.embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs
        )
        self.model_name = model_name
    
    def embed_documents(self, documents: List[Document]) -> List[List[float]]:
        """
        Generate embeddings for a list of documents.
        
        Args:
            documents: List of LangChain Document objects
            
        Returns:
            List of embedding vectors
        """
        texts = [doc.page_content for doc in documents]
        logger.info(f"Generating embeddings for {len(texts)} documents")
        
        try:
            embeddings = self.embeddings.embed_documents(texts)
            logger.info(f"Successfully generated {len(embeddings)} embeddings")
            return embeddings
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            raise
    
    def embed_query(self, query: str) -> List[float]:
        """
        Generate embedding for a single query.
        
        Args:
            query: Query text
            
        Returns:
            Embedding vector
        """
        try:
            embedding = self.embeddings.embed_query(query)
            return embedding
        except Exception as e:
            logger.error(f"Error generating query embedding: {e}")
            raise
    
    def get_embedding_dimension(self) -> int:
        """Get the dimension of embeddings produced by this model."""
        # Test embedding to get dimension
        test_embedding = self.embed_query("test")
        return len(test_embedding)

