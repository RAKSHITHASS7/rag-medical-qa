# PowerShell script to install dependencies on Windows
# This script handles the llama-cpp-python installation issue

Write-Host "🚀 Installing RAG Medical QA Dependencies for Windows" -ForegroundColor Green
Write-Host ""

# Upgrade pip first
Write-Host "📦 Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Install main dependencies (excluding llama-cpp-python)
Write-Host "`n📦 Installing main dependencies..." -ForegroundColor Yellow
pip install langchain==0.0.350
pip install langchain-community==0.0.10
pip install faiss-cpu==1.7.4
pip install sentence-transformers==2.2.2
pip install transformers==4.35.2
pip install torch==2.1.0
pip install PyPDF2==3.0.1
pip install pypdf==3.17.0
pip install rouge-score==0.1.2
pip install streamlit==1.28.1
pip install numpy==1.24.3
pip install pandas==2.0.3
pip install tqdm==4.66.1
pip install python-dotenv==1.0.0

# Install llama-cpp-python with pre-built wheel
Write-Host "`n📦 Installing llama-cpp-python (this may take a few minutes)..." -ForegroundColor Yellow
Write-Host "Using pre-built wheel for Windows..." -ForegroundColor Cyan

try {
    pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu
    Write-Host "✅ llama-cpp-python installed successfully!" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to install llama-cpp-python with pre-built wheel" -ForegroundColor Red
    Write-Host "`nTrying alternative installation method..." -ForegroundColor Yellow
    
    # Try direct installation
    try {
        pip install llama-cpp-python
        Write-Host "✅ llama-cpp-python installed successfully!" -ForegroundColor Green
    } catch {
        Write-Host "❌ Failed to install llama-cpp-python" -ForegroundColor Red
        Write-Host "`nPlease install manually:" -ForegroundColor Yellow
        Write-Host "  Option 1: pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu" -ForegroundColor Cyan
        Write-Host "  Option 2: Install Visual Studio Build Tools and try: pip install llama-cpp-python" -ForegroundColor Cyan
        Write-Host "  See INSTALL_WINDOWS.md for detailed instructions" -ForegroundColor Cyan
    }
}

# Verify installation
Write-Host "`n🔍 Verifying installation..." -ForegroundColor Yellow
python -c "import langchain; import faiss; import streamlit; print('✅ Core dependencies installed')" 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Core dependencies verified!" -ForegroundColor Green
} else {
    Write-Host "⚠️  Some dependencies may not be installed correctly" -ForegroundColor Yellow
}

# Check llama-cpp-python
Write-Host "`n🔍 Checking llama-cpp-python..." -ForegroundColor Yellow
python -c "from llama_cpp import Llama; print('✅ llama-cpp-python installed and working!')" 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ llama-cpp-python verified!" -ForegroundColor Green
} else {
    Write-Host "⚠️  llama-cpp-python not installed or not working" -ForegroundColor Yellow
    Write-Host "   You can still use the system but will need to install it later" -ForegroundColor Yellow
}

Write-Host "`n✨ Installation complete!" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Cyan
Write-Host "  1. Download Llama-3 GGUF model to models/ directory" -ForegroundColor White
Write-Host "  2. Place PDF files in data/pdfs/ directory" -ForegroundColor White
Write-Host "  3. Run: streamlit run app.py" -ForegroundColor White





