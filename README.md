# Medical RAG Question Answering System

A production-grade Retrieval-Augmented Generation (RAG) system for medical question answering, designed to provide fast, reliable, and citation-grounded answers from large medical research PDFs without hallucinations.
DEMO https://rag-medical-app.streamlit.app/

## 🎯 Features

- **PDF Document Ingestion**: Process medical research PDFs with page-level metadata
- **Semantic Search**: FAISS-based vector search with top-k retrieval
- **Local LLM Inference**: Llama-3 model running locally (no external APIs)
- **Anti-Hallucination**: Strict prompting to ensure answers are grounded in source documents
- **Citation Support**: Answers include source documents and page numbers
- **Evaluation Metrics**: ROUGE scores and faithfulness metrics for system evaluation
- **Streamlit UI**: User-friendly interface for querying and document management

## 🏗️ Architecture

```
rag-medical-qa/
├── src/
│   ├── ingestion/          # PDF processing and chunking
│   │   ├── pdf_processor.py
│   │   └── chunker.py
│   ├── embeddings/          # Embedding generation and indexing
│   │   ├── embedder.py
│   │   └── indexer.py
│   ├── retrieval/           # Semantic search
│   │   └── retriever.py
│   ├── generation/          # LLM inference
│   │   └── generator.py
│   ├── evaluation/          # Metrics and evaluation
│   │   └── evaluator.py
│   └── rag_pipeline.py      # Main pipeline orchestrator
├── app.py                   # Streamlit UI
├── requirements.txt
└── README.md
```

## 📋 Prerequisites

- Python 3.10 or higher
- 8GB+ RAM (16GB recommended for Llama-3)
- CUDA-capable GPU (optional, for faster inference)

## 🚀 Installation

1. **Clone the repository** (or navigate to project directory):
```bash
cd rag-medical-qa
```

2. **Create a virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:

**For Windows users:** See [INSTALL_WINDOWS.md](INSTALL_WINDOWS.md) for special instructions regarding `llama-cpp-python`.

```bash
# Standard installation (Linux/Mac)
pip install -r requirements.txt

# Windows: Use the provided script or see INSTALL_WINDOWS.md
# Option 1: Run the PowerShell script
.\install_windows.ps1

# Option 2: Manual installation
pip install --upgrade pip
pip install -r requirements.txt
# Then install llama-cpp-python separately:
pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu
```

4. **Download Llama-3 Model**:
   - Download a Llama-3 GGUF quantized model from [HuggingFace](https://huggingface.co/models?search=llama-3-gguf)
   - Recommended: `llama-3-8b-instruct-q4_0.gguf` or similar
   - Place it in `models/` directory
   - Example: `models/llama-3-8b-instruct-q4_0.gguf`

## 📖 Usage

### 1. Prepare Documents

Place your medical research PDFs in a directory:
```bash
mkdir -p data/pdfs
# Copy your PDF files to data/pdfs/
```

### 2. Run the Streamlit App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### 3. Ingest Documents

1. Navigate to the **"📥 Ingest Documents"** tab
2. Enter the path to your PDF directory (e.g., `data/pdfs/`)
3. Click **"Ingest Documents"**
4. Wait for processing to complete

### 4. Query the System

1. Navigate to the **"🔍 Query"** tab
2. Enter your medical question
3. Click **"Get Answer"**
4. View the answer with citations

## 🔧 Configuration

### Model Configuration

Edit `app.py` or use the sidebar to configure:
- **Model Path**: Path to Llama-3 GGUF model
- **Index Path**: Path to save/load FAISS index
- **Retrieval K**: Number of documents to retrieve (default: 5)

### Pipeline Configuration

Modify `RAGPipeline` initialization in `src/rag_pipeline.py`:
- `chunk_size`: Document chunk size (default: 1000)
- `chunk_overlap`: Overlap between chunks (default: 200)
- `embedding_model`: HuggingFace embedding model (default: `all-MiniLM-L6-v2`)

## 📊 Evaluation

The system includes evaluation metrics:

- **ROUGE Scores**: Measures overlap between generated and reference answers
  - ROUGE-1: Unigram overlap
  - ROUGE-2: Bigram overlap
  - ROUGE-L: Longest common subsequence

- **Faithfulness**: Measures how well answers are grounded in source context
  - Grounded sentence ratio
  - Context alignment score

Example evaluation usage:
```python
from src.evaluation import RAGEvaluator

evaluator = RAGEvaluator()
results = evaluator.evaluate_rag_pipeline(
    questions=["What is diabetes?"],
    generated_answers=["Diabetes is..."],
    reference_answers=["Diabetes is a metabolic disorder..."],
    contexts=["..."]
)
```

## 🏭 Production Considerations

### Performance Optimization

1. **GPU Acceleration**: Use CUDA-enabled PyTorch for faster embeddings
2. **Model Quantization**: Use quantized GGUF models (Q4, Q5) for faster inference
3. **Batch Processing**: Process multiple queries in batch
4. **Caching**: Implement response caching for common queries

### Scalability

- **Distributed FAISS**: Use FAISS with GPU support for large-scale indices
- **Async Processing**: Implement async document processing
- **Database Integration**: Store metadata in a database instead of in-memory

### Monitoring

- Add logging for all pipeline stages
- Track query latency and accuracy metrics
- Monitor model inference time and memory usage

## 🧪 Testing

Run tests (when implemented):
```bash
pytest tests/
```

## 📝 Code Structure

### Core Modules

- **`ingestion/`**: Handles PDF processing and document chunking
- **`embeddings/`**: Manages embedding generation and FAISS indexing
- **`retrieval/`**: Implements semantic search with top-k retrieval
- **`generation/`**: LLM inference with anti-hallucination prompts
- **`evaluation/`**: Computes ROUGE and faithfulness metrics

### Key Classes

- `RAGPipeline`: Main orchestrator for the complete pipeline
- `PDFProcessor`: Extracts text from PDFs with metadata
- `DocumentChunker`: Splits documents into chunks with overlap
- `Embedder`: Generates embeddings using HuggingFace models
- `VectorIndexer`: Manages FAISS vector store
- `Retriever`: Performs semantic search
- `AnswerGenerator`: Generates answers using Llama-3
- `RAGEvaluator`: Computes evaluation metrics

## 🔒 Anti-Hallucination Strategy

The system uses multiple strategies to prevent hallucinations:

1. **Strict Prompting**: Explicit instructions to only use provided context
2. **Citation Requirements**: All answers must cite source documents
3. **Context Filtering**: Only retrieved documents are used for generation
4. **Low Temperature**: Deterministic generation (temperature=0.1)
5. **Faithfulness Evaluation**: Metrics to measure grounding in context

## 🤝 Contributing

This is a production-ready codebase designed for:
- Resume projects
- Interview demonstrations
- Real-world healthcare applications

## 📄 License

This project is designed for educational and professional use.

## 🙏 Acknowledgments

- LangChain for RAG framework
- HuggingFace for embedding models
- FAISS for vector search
- Llama-3 for local LLM inference
- Streamlit for UI framework

## 📞 Support

For issues or questions, please check:
1. Model path configuration
2. Index path and existence
3. PDF file format and accessibility
4. System memory and resources

---


