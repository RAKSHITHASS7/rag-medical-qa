"""Example usage of the RAG Medical QA System."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.rag_pipeline import RAGPipeline
from src.evaluation import RAGEvaluator


def main():
    """Example usage demonstration."""
    
    # Configuration
    model_path = "models/llama-3-8b-instruct-q4_0.gguf"  # Update with your model path
    index_path = "models/faiss_index"
    pdf_path = "data/pdfs/"  # Directory containing PDFs
    
    # Initialize pipeline
    print("Initializing RAG Pipeline...")
    pipeline = RAGPipeline(
        model_path=model_path,
        index_path=index_path,
        embedding_model="sentence-transformers/all-MiniLM-L6-v2",
        chunk_size=1000,
        chunk_overlap=200,
        retrieval_k=5
    )
    
    # Option 1: Ingest documents (run once)
    print("\nIngesting documents...")
    try:
        pipeline.ingest_documents(pdf_path)
        print("✅ Documents ingested successfully!")
    except Exception as e:
        print(f"⚠️  Ingestion error (may already exist): {e}")
    
    # Option 2: Load existing index
    print("\nLoading index...")
    try:
        pipeline.load_index()
        print("✅ Index loaded successfully!")
    except Exception as e:
        print(f"❌ Error loading index: {e}")
        return
    
    # Query the system
    print("\n" + "="*50)
    print("Querying the RAG System")
    print("="*50)
    
    questions = [
        "What are the symptoms of diabetes?",
        "How is hypertension treated?",
        "What are the risk factors for cardiovascular disease?"
    ]
    
    for question in questions:
        print(f"\n❓ Question: {question}")
        print("-" * 50)
        
        try:
            response = pipeline.query(question, k=5)
            
            print(f"💡 Answer: {response['answer']}")
            print(f"\n📚 Citations ({len(response.get('citations', []))}):")
            
            for citation in response.get('citations', []):
                print(f"  [{citation['index']}] {citation['source']} - Page {citation['page_number']}")
        
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Evaluation example
    print("\n" + "="*50)
    print("Evaluation Example")
    print("="*50)
    
    evaluator = RAGEvaluator()
    
    # Example evaluation
    questions = ["What is diabetes?"]
    generated_answers = ["Diabetes is a metabolic disorder..."]
    reference_answers = ["Diabetes is a chronic metabolic disorder characterized by high blood sugar levels."]
    contexts = ["Diabetes is a chronic metabolic disorder..."]
    
    results = evaluator.evaluate_rag_pipeline(
        questions=questions,
        generated_answers=generated_answers,
        reference_answers=reference_answers,
        contexts=contexts
    )
    
    print(f"\n📊 Evaluation Results:")
    print(f"  Questions evaluated: {results['num_questions']}")
    if 'rouge' in results['metrics']:
        print(f"  ROUGE-1 F1: {results['metrics']['rouge']['rouge1']['fmeasure']:.3f}")
        print(f"  ROUGE-2 F1: {results['metrics']['rouge']['rouge2']['fmeasure']:.3f}")
        print(f"  ROUGE-L F1: {results['metrics']['rouge']['rougeL']['fmeasure']:.3f}")
    if 'faithfulness' in results['metrics']:
        print(f"  Faithfulness: {results['metrics']['faithfulness']['mean']:.3f}")


if __name__ == "__main__":
    main()

