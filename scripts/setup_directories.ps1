# PowerShell script to create necessary directories

New-Item -ItemType Directory -Force -Path "data\pdfs"
New-Item -ItemType Directory -Force -Path "models"
New-Item -ItemType Directory -Force -Path "logs"

Write-Host "Directories created successfully!"
Write-Host "Next steps:"
Write-Host "1. Place your PDF files in data\pdfs\"
Write-Host "2. Download Llama-3 GGUF model to models\"
Write-Host "3. Run: streamlit run app.py"

