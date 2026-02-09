"""Streamlit UI for Medical RAG Question Answering System."""

import streamlit as st
import logging
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.rag_pipeline import RAGPipeline
from src.evaluation import RAGEvaluator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Medical RAG QA System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS
st.markdown("""
    <style>
    /* Main Header */
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        padding: 1rem 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Answer Box */
    .answer-box {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
        border-radius: 15px;
        border-left: 5px solid #667eea;
        margin: 1.5rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        font-size: 1.1rem;
        line-height: 1.8;
    }
    
    /* Citation Box */
    .citation-box {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }
    
    .citation-box:hover {
        border-color: #667eea;
        box-shadow: 0 4px 8px rgba(102, 126, 234, 0.2);
        transform: translateY(-2px);
    }
    
    /* Status Badge */
    .status-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
        margin: 0.25rem;
    }
    
    .status-success {
        background: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    
    .status-error {
        background: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
    
    .status-warning {
        background: #fff3cd;
        color: #856404;
        border: 1px solid #ffeaa7;
    }
    
    /* Info Card */
    .info-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Section Header */
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #333;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #667eea;
    }
    
    /* Button Enhancements */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Sidebar Enhancements */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 1rem 2rem;
        font-weight: 600;
    }
    
    /* Input Field Styling */
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        padding: 0.5rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Text Area Styling */
    .stTextArea > div > div > textarea {
        border-radius: 8px;
        border: 2px solid #e0e0e0;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Metric Cards */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #667eea;
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #764ba2;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_rag_pipeline(model_path: str, index_path: str):
    """Load RAG pipeline with caching."""
    try:
        pipeline = RAGPipeline(
            model_path=model_path,
            index_path=index_path
        )
        pipeline.load_index()
        return pipeline
    except Exception as e:
        st.error(f"Error loading RAG pipeline: {e}")
        return None


def main():
    """Main Streamlit application."""
    
    # Header with enhanced styling
    st.markdown("""
    <div class="main-header">
        🏥 Medical RAG Question Answering System
    </div>
    <div style="text-align: center; color: #666; margin-bottom: 2rem; font-size: 1.1rem;">
        Powered by LangChain • FAISS • Llama-3
    </div>
    """, unsafe_allow_html=True)
    
    # Show ingest banner if index not found (will be updated after sidebar)
    # Check session state for index status
    index_exists_banner = st.session_state.get('index_exists', False)
    if not index_exists_banner:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1.5rem; border-radius: 10px; margin-bottom: 2rem; text-align: center;">
            <h3 style="color: white; margin: 0 0 1rem 0;">🚀 Get Started: Ingest Documents First!</h3>
            <p style="color: white; margin: 0; font-size: 1.1rem;">
                No index found. Please ingest PDF documents to build the knowledge base before querying.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Model Selection
        model_type = st.selectbox(
            "Model Type",
            ["Demo Mode (No LLM)", "Llama-3", "Custom Model"],
            help="Select the model type to use"
        )
        
        if model_type == "Demo Mode (No LLM)":
            model_path = "demo_mode"
            st.info("💡 Using context extraction (no LLM required)")
        elif model_type == "Llama-3":
            model_path = st.text_input(
                "Llama-3 Model Path",
                value="models/llama-3-8b-instruct-q4_0.gguf",
                help="Path to Llama-3 GGUF model file"
            )
        else:  # Custom Model
            model_path = st.text_input(
                "Custom Model Path",
                value="models/custom_model.gguf",
                help="Path to your custom GGUF model file"
            )
        
        st.markdown("---")
        
        # Index Management
        st.subheader("📊 Index Management")
        index_path = st.text_input(
            "FAISS Index Path",
            value="models/faiss_index",
            help="Path to FAISS vector index"
        )
        
        # Index actions
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Refresh Index"):
                st.cache_resource.clear()
                st.success("Index cache cleared")
        
        with col2:
            if st.button("🗑️ Delete Index"):
                import shutil
                if Path(index_path).exists():
                    shutil.rmtree(index_path)
                    st.success("Index deleted")
                else:
                    st.warning("Index not found")
        
        st.markdown("---")
        
        # Dataset Management
        st.subheader("📚 Dataset Management")
        dataset_path = st.text_input(
            "Dataset/PDF Directory",
            value="data/pdfs/",
            help="Path to directory containing PDF files"
        )
        
        # Show available datasets
        if Path(dataset_path).exists():
            pdf_files = list(Path(dataset_path).glob("*.pdf"))
            if pdf_files:
                st.success(f"✓ Found {len(pdf_files)} PDF files")
                with st.expander("📄 View PDF Files"):
                    for pdf in pdf_files[:10]:  # Show first 10
                        st.text(f"  • {pdf.name}")
                    if len(pdf_files) > 10:
                        st.caption(f"... and {len(pdf_files) - 10} more")
            else:
                st.warning("⚠ No PDF files found")
        else:
            st.error("✗ Directory not found")
        
        retrieval_k = st.slider(
            "Number of Documents to Retrieve",
            min_value=1,
            max_value=10,
            value=5,
            help="Top-k documents for retrieval"
        )
        
        # Advanced Settings
        with st.expander("⚙️ Advanced Settings"):
            chunk_size = st.slider(
                "Chunk Size",
                min_value=500,
                max_value=2000,
                value=1000,
                step=100,
                help="Size of document chunks"
            )
            chunk_overlap = st.slider(
                "Chunk Overlap",
                min_value=0,
                max_value=500,
                value=200,
                step=50,
                help="Overlap between chunks"
            )
            embedding_model = st.selectbox(
                "Embedding Model",
                [
                    "sentence-transformers/all-MiniLM-L6-v2",
                    "sentence-transformers/all-mpnet-base-v2",
                    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
                ],
                help="Model for generating embeddings"
            )
        
        st.markdown("---")
        st.header("📊 System Status")
        
        # Check if paths exist
        model_exists = (Path(model_path).exists() if model_path and model_path != "demo_mode" else False) or (model_path == "demo_mode")
        index_exists = Path(index_path).exists() if index_path else False
        
        # Store in session state for banner check
        st.session_state['index_exists'] = index_exists
        st.session_state['index_path'] = index_path
        
        # Enhanced status display
        st.markdown("### 📊 Status")
        
        if model_path == "demo_mode":
            st.markdown('<div class="status-badge status-success">✓ Demo Mode Active</div>', unsafe_allow_html=True)
            st.caption("Using context extraction (no LLM)")
        elif model_exists:
            st.markdown('<div class="status-badge status-success">✓ Model Found</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-badge status-error">✗ Model Not Found</div>', unsafe_allow_html=True)
            st.caption("Download Llama-3 GGUF model to models/")
        
        if index_exists:
            st.markdown('<div class="status-badge status-success">✓ Index Found</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-badge status-warning">⚠ Index Not Found</div>', unsafe_allow_html=True)
            st.caption("Ingest documents first")
    
    # Main content area
    tab1, tab2, tab3 = st.tabs(["🔍 Query", "📥 Ingest Documents", "📈 Evaluation"])
    
    # Query Tab
    with tab1:
        st.markdown('<div class="section-header">🔍 Ask a Medical Question</div>', unsafe_allow_html=True)
        
        if not index_exists:
            st.markdown("""
            <div class="info-card">
                <strong>⚠️ Setup Required</strong><br>
                Please ingest documents first to build the knowledge base before querying.
            </div>
            """, unsafe_allow_html=True)
            
            # Quick Ingest Section
            st.markdown("---")
            st.markdown('<div class="section-header">🚀 Quick Ingest</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns([2, 1])
            with col1:
                quick_pdf_path = st.text_input(
                    "PDF Path:",
                    value="data/pdfs/",
                    key="quick_ingest_path",
                    help="Path to PDF file or directory"
                )
            
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("📥 Ingest Now", type="primary", use_container_width=True, key="quick_ingest_btn"):
                    if quick_pdf_path:
                        with st.spinner("Processing PDFs and creating index... This may take 1-3 minutes..."):
                            try:
                                pipeline = RAGPipeline(
                                    model_path=model_path if model_path != "demo_mode" else "demo.gguf",
                                    index_path=index_path
                                )
                                pipeline.ingest_documents(quick_pdf_path)
                                
                                st.success("✅ Successfully ingested documents! Index created.")
                                st.info("💡 Refresh the page or go to Query tab to start asking questions.")
                                st.balloons()
                                
                                # Clear cache
                                st.cache_resource.clear()
                                
                                # Auto-refresh after 2 seconds
                                import time
                                time.sleep(2)
                                st.rerun()
                                
                            except Exception as e:
                                st.error(f"❌ Error ingesting documents: {e}")
                                st.info("💡 Make sure PDF files exist in the specified path.")
                    else:
                        st.warning("Please provide a PDF path.")
            
            # Show available PDFs
            if Path(quick_pdf_path).exists():
                pdf_files = list(Path(quick_pdf_path).glob("*.pdf"))
                if pdf_files:
                    st.info(f"📚 Found {len(pdf_files)} PDF file(s) ready to ingest:")
                    for pdf in pdf_files[:5]:
                        st.text(f"   • {pdf.name}")
                    if len(pdf_files) > 5:
                        st.caption(f"   ... and {len(pdf_files) - 5} more")
                else:
                    st.warning("⚠️ No PDF files found in this directory.")
        elif not model_exists:
            st.markdown("""
            <div class="info-card">
                <strong>⚠️ Model Setup Required</strong><br>
                To enable querying, you need to install llama-cpp-python and download a Llama-3 model.
            </div>
            """, unsafe_allow_html=True)
            with st.expander("📋 Setup Instructions", expanded=True):
                st.markdown("""
                **Step 1: Install llama-cpp-python**
                ```powershell
                pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu
                ```
                
                **Step 2: Download Llama-3 Model**
                - Visit: https://huggingface.co/models?search=llama-3-gguf
                - Download: `llama-3-8b-instruct-q4_0.gguf` (recommended)
                - Place in: `models/` directory
                
                **Step 3: Update Model Path**
                - Update the model path in the sidebar to match your downloaded file
                """)
        else:
            # Load pipeline
            pipeline = load_rag_pipeline(model_path, index_path)
            
            if pipeline is None:
                st.error("Failed to load RAG pipeline. Please check your configuration.")
            else:
                # Query input
                question = st.text_area(
                    "Enter your medical question:",
                    height=100,
                    placeholder="e.g., What are the symptoms of diabetes?"
                )
                
                if st.button("🔍 Get Answer", type="primary"):
                    if not question.strip():
                        st.warning("Please enter a question.")
                    else:
                        with st.spinner("Retrieving relevant documents and generating answer..."):
                            try:
                                # Query will automatically use demo mode if LLM not available
                                response = pipeline.query(question, k=retrieval_k)
                                
                                # Show demo mode notice if applicable
                                if response.get("model") == "Demo Mode (Context Extraction)":
                                    st.info("💡 **Demo Mode**: Using context extraction (LLM not available). Install llama-cpp-python for full LLM answers.")
                                
                                # Display answer with enhanced styling
                                st.markdown('<div class="section-header">💡 Answer</div>', unsafe_allow_html=True)
                                st.markdown(f'<div class="answer-box">{response["answer"]}</div>', unsafe_allow_html=True)
                                
                                # Display citations with enhanced styling
                                if response.get("citations"):
                                    st.markdown('<div class="section-header">📚 Sources & Citations</div>', unsafe_allow_html=True)
                                    for citation in response["citations"]:
                                        st.markdown(f"""
                                        <div class="citation-box">
                                            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                                                <span style="background: #667eea; color: white; padding: 0.25rem 0.75rem; border-radius: 20px; font-weight: 600; margin-right: 1rem;">
                                                    [{citation['index']}]
                                                </span>
                                                <strong style="color: #333; font-size: 1.1rem;">
                                                    {citation['source']}
                                                </strong>
                                                <span style="margin-left: auto; color: #666; font-size: 0.9rem;">
                                                    Page {citation['page_number']}
                                                </span>
                                            </div>
                                            <div style="color: #555; font-size: 0.95rem; margin-top: 0.5rem; padding-left: 1rem; border-left: 3px solid #e0e0e0;">
                                                {citation['preview']}
                                            </div>
                                        </div>
                                        """, unsafe_allow_html=True)
                                
                                # Metadata
                                with st.expander("📊 Response Metadata"):
                                    st.json({
                                        "Question": response["question"],
                                        "Context Length": response["context_length"],
                                        "Number of Citations": len(response.get("citations", [])),
                                        "Model": response.get("model", "Unknown")
                                    })
                            
                            except Exception as e:
                                st.error(f"Error generating answer: {e}")
                                logger.exception("Error in query")
    
    # Ingestion Tab
    with tab2:
        st.markdown('<div class="section-header">📥 Document Ingestion & Dataset Management</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="info-card">
            <strong>📋 Instructions:</strong><br>
            Upload or process PDF documents to build the knowledge base. 
            The system will extract text, create embeddings, and build a searchable vector index.
        </div>
        """, unsafe_allow_html=True)
        
        # Dataset selection
        col1, col2 = st.columns([2, 1])
        with col1:
            pdf_path = st.text_input(
                "PDF Path (file or directory):",
                value=dataset_path if 'dataset_path' in locals() else "data/pdfs/",
                help="Path to PDF file or directory containing PDFs"
            )
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("📂 Browse", use_container_width=True):
                st.info("💡 Enter the path manually or use the sidebar dataset path")
        
        # Show dataset info
        if Path(pdf_path).exists():
            if Path(pdf_path).is_dir():
                pdf_files = list(Path(pdf_path).glob("*.pdf"))
                st.info(f"📚 Found {len(pdf_files)} PDF file(s) in directory")
                
                if pdf_files:
                    with st.expander("📄 View PDF Files"):
                        for pdf in pdf_files:
                            file_size = pdf.stat().st_size / (1024 * 1024)  # MB
                            st.text(f"  • {pdf.name} ({file_size:.2f} MB)")
            elif Path(pdf_path).is_file() and pdf_path.endswith('.pdf'):
                file_size = Path(pdf_path).stat().st_size / (1024 * 1024)
                st.info(f"📄 Selected: {Path(pdf_path).name} ({file_size:.2f} MB)")
        
        # Upload new PDF
        st.markdown("---")
        st.subheader("📤 Upload New PDF")
        uploaded_file = st.file_uploader(
            "Choose a PDF file",
            type=['pdf'],
            help="Upload a new PDF file to add to the dataset"
        )
        
        if uploaded_file is not None:
            # Save uploaded file
            upload_path = Path("data/pdfs") / uploaded_file.name
            upload_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(upload_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            st.success(f"✅ Uploaded: {uploaded_file.name}")
            st.info(f"💡 File saved to: {upload_path}")
            
            # Auto-update path
            pdf_path = str(upload_path.parent)
        
        if st.button("📥 Ingest Documents", type="primary"):
            if not pdf_path:
                st.warning("Please provide a PDF path.")
            else:
                try:
                    with st.spinner("Processing PDFs and creating vector index..."):
                        # For ingestion, we don't need the LLM, so model path can be placeholder
                        # The generator won't be initialized until querying
                        # Get advanced settings if available
                        chunk_size_val = chunk_size if 'chunk_size' in locals() else 1000
                        chunk_overlap_val = chunk_overlap if 'chunk_overlap' in locals() else 200
                        embedding_model_val = embedding_model if 'embedding_model' in locals() else "sentence-transformers/all-MiniLM-L6-v2"
                        
                        pipeline = RAGPipeline(
                            model_path=model_path if model_path != "demo_mode" else "demo.gguf",
                            index_path=index_path,
                            chunk_size=chunk_size_val,
                            chunk_overlap=chunk_overlap_val,
                            embedding_model=embedding_model_val
                        )
                        pipeline.ingest_documents(pdf_path)
                        
                        st.success(f"✅ Successfully ingested documents from {pdf_path}")
                        st.info("You can now use the Query tab to ask questions.")
                        st.info("💡 **Note:** You'll need to install llama-cpp-python and download a model to query.")
                        
                        # Clear cache to reload pipeline
                        st.cache_resource.clear()
                
                except Exception as e:
                    st.error(f"Error ingesting documents: {e}")
                    logger.exception("Error in ingestion")
                    st.info("💡 **Tip:** Make sure PDF files exist in the specified path.")
    
    # Evaluation Tab
    with tab3:
        st.markdown('<div class="section-header">📈 System Evaluation & Metrics</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="info-card">
            <strong>📊 Evaluation Metrics:</strong><br>
            Evaluate the RAG system using ROUGE scores and faithfulness metrics to measure 
            answer quality and grounding in source documents.
        </div>
        """, unsafe_allow_html=True)
        
        # Evaluation Dataset Input
        st.subheader("📋 Evaluation Dataset")
        
        eval_mode = st.radio(
            "Evaluation Mode",
            ["Manual Input", "File Upload", "Quick Test"],
            horizontal=True
        )
        
        if eval_mode == "Manual Input":
            st.markdown("**Enter evaluation data:**")
            
            col1, col2 = st.columns(2)
            with col1:
                questions_text = st.text_area(
                    "Questions (one per line):",
                    height=150,
                    placeholder="What is diabetes?\nWhat are the symptoms of hypertension?\nHow is cardiovascular disease prevented?"
                )
            
            with col2:
                reference_text = st.text_area(
                    "Reference Answers (one per line):",
                    height=150,
                    placeholder="Diabetes is a chronic metabolic disorder...\nHypertension symptoms include...\nPrevention includes..."
                )
            
            if st.button("📊 Run Evaluation", type="primary"):
                if questions_text and reference_text:
                    questions = [q.strip() for q in questions_text.split('\n') if q.strip()]
                    references = [r.strip() for r in reference_text.split('\n') if r.strip()]
                    
                    if len(questions) == len(references):
                        with st.spinner("Evaluating..."):
                            # Generate answers
                            if index_exists and model_exists:
                                pipeline = load_rag_pipeline(model_path, index_path)
                                if pipeline:
                                    generated_answers = []
                                    contexts_list = []
                                    
                                    for question in questions:
                                        try:
                                            response = pipeline.query(question, k=retrieval_k)
                                            generated_answers.append(response['answer'])
                                            # Get context (simplified)
                                            contexts_list.append(response.get('context', ''))
                                        except Exception as e:
                                            generated_answers.append(f"Error: {e}")
                                            contexts_list.append("")
                                    
                                    # Evaluate
                                    evaluator = RAGEvaluator()
                                    results = evaluator.evaluate_rag_pipeline(
                                        questions=questions,
                                        generated_answers=generated_answers,
                                        reference_answers=references,
                                        contexts=contexts_list if contexts_list else None
                                    )
                                    
                                    # Display results
                                    st.success("✅ Evaluation Complete!")
                                    
                                    col1, col2, col3 = st.columns(3)
                                    if 'rouge' in results['metrics']:
                                        rouge = results['metrics']['rouge']
                                        with col1:
                                            st.metric("ROUGE-1 F1", f"{rouge['rouge1']['fmeasure']:.3f}")
                                        with col2:
                                            st.metric("ROUGE-2 F1", f"{rouge['rouge2']['fmeasure']:.3f}")
                                        with col3:
                                            st.metric("ROUGE-L F1", f"{rouge['rougeL']['fmeasure']:.3f}")
                                    
                                    if 'faithfulness' in results['metrics']:
                                        st.metric("Faithfulness Score", f"{results['metrics']['faithfulness']['mean']:.3f}")
                                    
                                    with st.expander("📊 Detailed Results"):
                                        st.json(results)
                                else:
                                    st.error("Failed to load pipeline")
                            else:
                                st.warning("Please ingest documents and set up model first")
                    else:
                        st.error("Number of questions and references must match")
                else:
                    st.warning("Please provide both questions and reference answers")
        
        elif eval_mode == "File Upload":
            st.info("💡 Upload a CSV file with columns: question, reference_answer")
            uploaded_eval = st.file_uploader("Upload Evaluation Dataset", type=['csv'])
            
            # Show sample dataset
            sample_path = Path("data/evaluation_dataset.csv")
            if sample_path.exists():
                with st.expander("📄 View Sample Dataset"):
                    import pandas as pd
                    sample_df = pd.read_csv(sample_path)
                    st.dataframe(sample_df)
                    st.download_button(
                        "📥 Download Sample Dataset",
                        sample_df.to_csv(index=False),
                        "evaluation_dataset.csv",
                        "text/csv"
                    )
            
            if uploaded_eval:
                import pandas as pd
                df = pd.read_csv(uploaded_eval)
                
                st.success(f"✅ Loaded {len(df)} question-answer pairs")
                st.dataframe(df)
                
                # Validate columns
                required_cols = ['question', 'reference_answer']
                if all(col in df.columns for col in required_cols):
                    if st.button("📊 Run Evaluation on Uploaded Dataset", type="primary"):
                        if index_exists:
                            with st.spinner("Evaluating dataset..."):
                                pipeline = load_rag_pipeline(
                                    model_path if model_exists else "demo_mode", 
                                    index_path
                                )
                                if pipeline:
                                    questions = df['question'].tolist()
                                    references = df['reference_answer'].tolist()
                                    generated_answers = []
                                    contexts_list = []
                                    
                                    progress_bar = st.progress(0)
                                    for i, question in enumerate(questions):
                                        try:
                                            response = pipeline.query(question, k=retrieval_k)
                                            generated_answers.append(response['answer'])
                                            contexts_list.append(response.get('context', ''))
                                        except Exception as e:
                                            generated_answers.append(f"Error: {e}")
                                            contexts_list.append("")
                                        progress_bar.progress((i + 1) / len(questions))
                                    
                                    # Evaluate
                                    evaluator = RAGEvaluator()
                                    results = evaluator.evaluate_rag_pipeline(
                                        questions=questions,
                                        generated_answers=generated_answers,
                                        reference_answers=references,
                                        contexts=contexts_list if contexts_list else None
                                    )
                                    
                                    st.success("✅ Evaluation Complete!")
                                    
                                    # Display metrics
                                    col1, col2, col3, col4 = st.columns(4)
                                    if 'rouge' in results['metrics']:
                                        rouge = results['metrics']['rouge']
                                        with col1:
                                            st.metric("ROUGE-1 F1", f"{rouge['rouge1']['fmeasure']:.3f}")
                                        with col2:
                                            st.metric("ROUGE-2 F1", f"{rouge['rouge2']['fmeasure']:.3f}")
                                        with col3:
                                            st.metric("ROUGE-L F1", f"{rouge['rougeL']['fmeasure']:.3f}")
                                    
                                    if 'faithfulness' in results['metrics']:
                                        with col4:
                                            st.metric("Faithfulness", f"{results['metrics']['faithfulness']['mean']:.3f}")
                                    
                                    # Detailed results
                                    with st.expander("📊 Detailed Results"):
                                        st.json(results)
                                    
                                    # Results table
                                    results_df = pd.DataFrame({
                                        'Question': questions,
                                        'Generated Answer': generated_answers,
                                        'Reference Answer': references
                                    })
                                    st.dataframe(results_df)
                                else:
                                    st.error("Failed to load pipeline")
                        else:
                            st.warning("Please ingest documents first")
                else:
                    st.error(f"CSV must have columns: {', '.join(required_cols)}")
        
        else:  # Quick Test
            st.markdown("**Quick Test with Sample Questions:**")
            if st.button("🚀 Run Quick Test", type="primary"):
                if index_exists:
                    sample_questions = [
                        "What is diabetes?",
                        "What are the symptoms of hypertension?",
                        "How is cardiovascular disease prevented?"
                    ]
                    
                    pipeline = load_rag_pipeline(model_path if model_exists else "demo_mode", index_path)
                    if pipeline:
                        st.success("✅ Quick test completed!")
                        st.info("💡 Use Manual Input mode for full evaluation with reference answers")
                    else:
                        st.error("Failed to load pipeline")
                else:
                    st.warning("Please ingest documents first")
        
        # Metrics Info
        st.markdown("---")
        st.subheader("📊 Available Metrics")
        st.info("""
        **ROUGE Scores:**
        - ROUGE-1: Unigram overlap between generated and reference
        - ROUGE-2: Bigram overlap
        - ROUGE-L: Longest common subsequence
        
        **Faithfulness:**
        - Measures how well answers are grounded in source context
        - Higher score = more faithful to source documents
        """)


if __name__ == "__main__":
    main()
