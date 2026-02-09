"""FAISS vector index creation and management."""

import logging
import pickle
from pathlib import Path
from typing import List, Optional
import faiss
import numpy as np
from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from langchain_core.embeddings import Embeddings

logger = logging.getLogger(__name__)


class VectorIndexer:
    """Manages FAISS vector index creation, saving, and loading."""
    
    def __init__(self, embeddings: Embeddings, index_path: Optional[str] = None):
        """
        Initialize the vector indexer.
        
        Args:
            embeddings: LangChain embeddings instance
            index_path: Optional path to save/load index
        """
        self.embeddings = embeddings
        self.index_path = Path(index_path) if index_path else None
        self.vectorstore: Optional[FAISS] = None
    
    def create_index(self, documents: List[Document]) -> FAISS:
        """
        Create FAISS index from documents.
        
        Args:
            documents: List of LangChain Document objects
            
        Returns:
            FAISS vectorstore instance
        """
        if not documents:
            raise ValueError("Cannot create index from empty document list")
        
        logger.info(f"Creating FAISS index from {len(documents)} documents")
        
        try:
            self.vectorstore = FAISS.from_documents(
                documents=documents,
                embedding=self.embeddings
            )
            logger.info(f"Successfully created FAISS index with {len(documents)} vectors")
            return self.vectorstore
        except Exception as e:
            logger.error(f"Error creating FAISS index: {e}")
            raise
    
    def save_index(self, save_path: Optional[str] = None) -> None:
        """
        Save the FAISS index to disk.
        
        Args:
            save_path: Optional custom path to save index
        """
        if self.vectorstore is None:
            raise ValueError("No index to save. Create index first.")
        
        save_path = Path(save_path) if save_path else self.index_path
        if save_path is None:
            raise ValueError("No save path specified")
        
        save_path.parent.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Saving FAISS index to {save_path}")
        try:
            self.vectorstore.save_local(str(save_path))
            logger.info(f"Successfully saved index to {save_path}")
        except Exception as e:
            logger.error(f"Error saving index: {e}")
            raise
    
    def load_index(self, load_path: Optional[str] = None) -> FAISS:
        """
        Load FAISS index from disk.
        
        Args:
            load_path: Optional custom path to load index from
            
        Returns:
            FAISS vectorstore instance
        """
        load_path = Path(load_path) if load_path else self.index_path
        if load_path is None:
            raise ValueError("No load path specified")
        
        if not load_path.exists():
            raise FileNotFoundError(f"Index not found at {load_path}")
        
        logger.info(f"Loading FAISS index from {load_path}")
        try:
            self.vectorstore = FAISS.load_local(
                str(load_path),
                embeddings=self.embeddings
            )
            logger.info(f"Successfully loaded index from {load_path}")
            return self.vectorstore
        except Exception as e:
            logger.error(f"Error loading index: {e}")
            raise
    
    def get_vectorstore(self) -> FAISS:
        """Get the current vectorstore instance."""
        if self.vectorstore is None:
            raise ValueError("No vectorstore available. Create or load index first.")
        return self.vectorstore
    
    def add_documents(self, documents: List[Document]) -> None:
        """
        Add new documents to existing index.
        
        Args:
            documents: List of new documents to add
        """
        if self.vectorstore is None:
            raise ValueError("No existing index. Create index first.")
        
        logger.info(f"Adding {len(documents)} documents to existing index")
        try:
            self.vectorstore.add_documents(documents)
            logger.info(f"Successfully added {len(documents)} documents")
        except Exception as e:
            logger.error(f"Error adding documents: {e}")
            raise

