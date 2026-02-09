# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies

**Windows Users:** See [INSTALL_WINDOWS.md](INSTALL_WINDOWS.md) for special instructions.

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install packages
# Windows: Use install_windows.ps1 or follow INSTALL_WINDOWS.md
pip install -r requirements.txt

# Windows: If llama-cpp-python fails, install separately:
# pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu
```

### Step 2: Download Llama-3 Model

1. Download a quantized Llama-3 GGUF model:
   - Visit: https://huggingface.co/models?search=llama-3-gguf
   - Recommended: `llama-3-8b-instruct-q4_0.gguf` (smaller, faster)
   - Or: `llama-3-70b-instruct-q4_0.gguf` (larger, better quality)

2. Place the model file in `models/` directory:
   ```bash
   mkdir -p models
   # Copy your .gguf file to models/
   ```

### Step 3: Prepare PDF Documents

```bash
# Create PDF directory
mkdir -p data/pdfs

# Copy your medical research PDFs to data/pdfs/
```

### Step 4: Run the Application

```bash
streamlit run app.py
```

### Step 5: Ingest Documents

1. Open the app in your browser (usually `http://localhost:8501`)
2. Go to **"📥 Ingest Documents"** tab
3. Enter path: `data/pdfs/`
4. Click **"Ingest Documents"**
5. Wait for processing to complete

### Step 6: Ask Questions

1. Go to **"🔍 Query"** tab
2. Enter your medical question
3. Click **"Get Answer"**
4. View answer with citations!

## 🎯 Example Questions

- "What are the symptoms of diabetes?"
- "How is hypertension treated?"
- "What are the risk factors for cardiovascular disease?"
- "Explain the mechanism of action of metformin."

## ⚙️ Configuration

Edit `config.py` or create `.env` file to customize:
- Model paths
- Chunk sizes
- Retrieval parameters
- LLM settings

## 🐛 Troubleshooting

### Model Not Found
- Ensure Llama-3 GGUF file is in `models/` directory
- Check the model path in sidebar configuration

### Index Not Found
- Run document ingestion first
- Check that PDFs were processed successfully

### Out of Memory
- Use a smaller quantized model (Q4 instead of Q8)
- Reduce `LLM_N_CTX` in config
- Process fewer documents at once

### Slow Performance
- Use GPU if available (set `EMBEDDING_DEVICE=cuda`)
- Use smaller embedding model
- Reduce retrieval K value

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [examples/example_usage.py](examples/example_usage.py) for programmatic usage
- Review evaluation metrics in the Evaluation tab

---

**Happy Querying! 🏥**

