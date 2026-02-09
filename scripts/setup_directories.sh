#!/bin/bash
# Setup script to create necessary directories

mkdir -p data/pdfs
mkdir -p models
mkdir -p logs

echo "Directories created successfully!"
echo "Next steps:"
echo "1. Place your PDF files in data/pdfs/"
echo "2. Download Llama-3 GGUF model to models/"
echo "3. Run: streamlit run app.py"

