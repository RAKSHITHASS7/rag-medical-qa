# Quick script to run the Streamlit app
# This ensures we use the virtual environment Python

Write-Host "🚀 Starting Medical RAG QA System..." -ForegroundColor Green
Write-Host ""

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Run Streamlit using the venv Python
Write-Host "Starting Streamlit app..." -ForegroundColor Yellow
Write-Host "App will open at http://localhost:8501" -ForegroundColor Cyan
Write-Host ""

& .\venv\Scripts\python.exe -m streamlit run app.py




