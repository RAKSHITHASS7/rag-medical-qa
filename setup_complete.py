"""Complete setup script to make the project fully functional."""

import subprocess
import sys
from pathlib import Path

def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"\n{'='*60}")
    print(f"📋 {description}")
    print(f"{'='*60}")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ Success: {description}")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Warning: {e}")
        if e.stdout:
            print(e.stdout)
        if e.stderr:
            print(e.stderr)
        return False

def main():
    """Complete setup process."""
    print("🚀 Complete Project Setup")
    print("=" * 60)
    
    # Step 1: Create directories
    print("\n📁 Creating directories...")
    directories = ["data/pdfs", "models", "logs"]
    for dir_path in directories:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"  ✅ {dir_path}")
    
    # Step 2: Create sample PDF
    print("\n📄 Creating sample PDF...")
    try:
        from create_sample_pdf import create_sample_medical_pdf
        create_sample_medical_pdf()
        print("  ✅ Sample PDF created")
    except Exception as e:
        print(f"  ⚠️  Could not create sample PDF: {e}")
    
    # Step 3: Check dependencies
    print("\n📦 Checking dependencies...")
    dependencies = ["streamlit", "langchain", "faiss", "sentence_transformers"]
    missing = []
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"  ✅ {dep}")
        except ImportError:
            print(f"  ❌ {dep} - MISSING")
            missing.append(dep)
    
    if missing:
        print(f"\n⚠️  Missing dependencies: {', '.join(missing)}")
        print("   Run: pip install -r requirements.txt")
    
    # Step 4: Check llama-cpp-python
    print("\n🤖 Checking LLM support...")
    try:
        import llama_cpp
        print("  ✅ llama-cpp-python installed")
    except ImportError:
        print("  ⚠️  llama-cpp-python not installed (demo mode will be used)")
        print("     To enable full LLM: pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu")
    
    # Step 5: Summary
    print("\n" + "=" * 60)
    print("✨ Setup Complete!")
    print("=" * 60)
    print("\n📋 Next Steps:")
    print("  1. Run: streamlit run app.py")
    print("  2. Go to 'Ingest Documents' tab")
    print("  3. Click 'Ingest Documents' (sample PDF is ready)")
    print("  4. Go to 'Query' tab and test questions")
    print("\n💡 Demo mode works without LLM - you can test the system now!")
    print("   Full LLM mode requires llama-cpp-python and a model file.")

if __name__ == "__main__":
    main()




