"""Semantic search retrieval with top-k results."""

import logging
from typing import List, Dict, Optional
from langchain_community.vectorstores import FAISS
from langchain.schema import Document

logger = logging.getLogger(__name__)


class Retriever:
    """Retrieves relevant documents using semantic search."""
    
    def __init__(self, vectorstore: FAISS, k: int = 5, score_threshold: Optional[float] = None):
        """
        Initialize the retriever.
        
        Args:
            vectorstore: FAISS vectorstore instance
            k: Number of top documents to retrieve
            score_threshold: Optional minimum similarity score threshold
        """
        self.vectorstore = vectorstore
        self.k = k
        self.score_threshold = score_threshold
    
    def retrieve(self, query: str, k: Optional[int] = None) -> List[Document]:
        """
        Retrieve top-k relevant documents for a query.
        
        Args:
            query: Search query
            k: Optional override for number of results
            
        Returns:
            List of relevant Document objects
        """
        k = k if k is not None else self.k
        
        logger.info(f"Retrieving top-{k} documents for query: {query[:50]}...")
        
        try:
            # Use similarity_search_with_score to get scores
            results = self.vectorstore.similarity_search_with_score(query, k=k)
            
            # Filter by threshold if specified
            if self.score_threshold is not None:
                results = [(doc, score) for doc, score in results if score >= self.score_threshold]
            
            documents = [doc for doc, score in results]
            logger.info(f"Retrieved {len(documents)} documents")
            
            return documents
            
        except Exception as e:
            logger.error(f"Error retrieving documents: {e}")
            raise
    
    def retrieve_with_scores(self, query: str, k: Optional[int] = None) -> List[tuple]:
        """
        Retrieve documents with similarity scores.
        
        Args:
            query: Search query
            k: Optional override for number of results
            
        Returns:
            List of (Document, score) tuples
        """
        k = k if k is not None else self.k
        
        try:
            results = self.vectorstore.similarity_search_with_score(query, k=k)
            
            if self.score_threshold is not None:
                results = [(doc, score) for doc, score in results if score >= self.score_threshold]
            
            return results
        except Exception as e:
            logger.error(f"Error retrieving documents with scores: {e}")
            raise
    
    def format_context(self, documents: List[Document]) -> str:
        """
        Format retrieved documents into context string with citations.
        
        Args:
            documents: List of retrieved Document objects
            
        Returns:
            Formatted context string with citations
        """
        context_parts = []
        
        for idx, doc in enumerate(documents, start=1):
            source = doc.metadata.get('source', 'Unknown')
            page = doc.metadata.get('page_number', 'N/A')
            chunk_idx = doc.metadata.get('chunk_index', 'N/A')
            
            citation = f"[{idx}] Source: {source}, Page: {page}"
            if chunk_idx != 'N/A':
                citation += f", Chunk: {chunk_idx}"
            
            context_parts.append(f"{citation}\n{doc.page_content}")
        
        return "\n\n---\n\n".join(context_parts)
    
    def get_citations(self, documents: List[Document]) -> List[Dict[str, any]]:
        """
        Extract citation information from documents.
        
        Args:
            documents: List of retrieved Document objects
            
        Returns:
            List of citation dictionaries
        """
        citations = []
        
        for idx, doc in enumerate(documents, start=1):
            citations.append({
                'index': idx,
                'source': doc.metadata.get('source', 'Unknown'),
                'page_number': doc.metadata.get('page_number', 'N/A'),
                'chunk_index': doc.metadata.get('chunk_index', 'N/A'),
                'text_preview': doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
            })
        
        return citations

