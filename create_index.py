"""Script to automatically create the FAISS index from PDFs."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.rag_pipeline import RAGPipeline
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_index():
    """Create FAISS index from PDFs."""
    print("🚀 Creating FAISS Index")
    print("=" * 60)
    
    # Configuration
    pdf_path = "data/pdfs/"
    index_path = "models/faiss_index"
    model_path = "demo_mode"  # Use demo mode for ingestion
    
    # Check if PDFs exist
    pdf_dir = Path(pdf_path)
    if not pdf_dir.exists():
        print(f"❌ Error: PDF directory not found: {pdf_path}")
        return False
    
    pdf_files = list(pdf_dir.glob("*.pdf"))
    if not pdf_files:
        print(f"❌ Error: No PDF files found in {pdf_path}")
        return False
    
    print(f"📄 Found {len(pdf_files)} PDF file(s):")
    for pdf in pdf_files:
        print(f"   • {pdf.name}")
    
    print(f"\n📊 Index will be saved to: {index_path}")
    print("\n⏳ Processing PDFs and creating index...")
    print("   This may take 1-3 minutes...\n")
    
    try:
        # Create pipeline
        pipeline = RAGPipeline(
            model_path=model_path,
            index_path=index_path,
            chunk_size=1000,
            chunk_overlap=200
        )
        
        # Ingest documents
        pipeline.ingest_documents(pdf_path)
        
        print("\n" + "=" * 60)
        print("✅ SUCCESS! Index created successfully!")
        print("=" * 60)
        print(f"\n📊 Index location: {index_path}")
        print(f"📄 Documents processed: {len(pdf_files)}")
        print("\n💡 You can now use the Query tab in the Streamlit app!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error creating index: {e}")
        logger.exception("Error in index creation")
        return False

if __name__ == "__main__":
    success = create_index()
    sys.exit(0 if success else 1)




