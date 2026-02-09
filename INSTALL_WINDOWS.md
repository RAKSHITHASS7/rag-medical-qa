# Windows Installation Guide

## 🪟 Installing llama-cpp-python on Windows

The `llama-cpp-python` package requires compilation on Windows, which can be challenging. Here are several solutions:

### Option 1: Pre-built Wheels (Recommended - Easiest)

Use pre-built wheels from the official repository:

```powershell
# For CPU-only (recommended for most users)
pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu

# For CUDA (if you have NVIDIA GPU)
pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu121
```

### Option 2: Install Build Tools (For Compilation)

If pre-built wheels don't work, install Visual Studio Build Tools:

1. **Download Visual Studio Build Tools:**
   - Visit: https://visualstudio.microsoft.com/downloads/
   - Download "Build Tools for Visual Studio 2022"
   - During installation, select "C++ build tools"

2. **Install with pip:**
   ```powershell
   pip install llama-cpp-python
   ```

### Option 3: Use Conda (Alternative)

If you have Anaconda/Miniconda:

```powershell
conda install -c conda-forge llama-cpp-python
```

### Option 4: Make it Optional (Development Only)

If you want to test other parts of the system first, you can:

1. Comment out llama-cpp-python in `requirements.txt`
2. Install other dependencies: `pip install -r requirements.txt`
3. Install llama-cpp-python later using one of the methods above

## 🔧 Complete Installation Steps

1. **Upgrade pip first:**
   ```powershell
   python -m pip install --upgrade pip
   ```

2. **Install other dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Install llama-cpp-python separately:**
   ```powershell
   pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu
   ```

## ✅ Verify Installation

Test that llama-cpp-python is installed correctly:

```python
try:
    from llama_cpp import Llama
    print("✅ llama-cpp-python installed successfully!")
except ImportError as e:
    print(f"❌ Error: {e}")
```

## 🐛 Troubleshooting

### Error: "Microsoft Visual C++ 14.0 or greater is required"

**Solution:** Install Visual Studio Build Tools (Option 2 above)

### Error: "Failed building wheel"

**Solution:** Use pre-built wheels (Option 1 above)

### Error: "No module named 'llama_cpp'"

**Solution:** 
- Verify installation: `pip list | findstr llama`
- Reinstall: `pip uninstall llama-cpp-python && pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu`

### Out of Memory Errors

**Solution:**
- Use a smaller quantized model (Q4 instead of Q8)
- Reduce `n_ctx` parameter in generator
- Close other applications

## 📝 Alternative: Use Different LLM Backend

If llama-cpp-python continues to cause issues, you can modify the system to use:

- **Ollama** (easier installation, local inference)
- **HuggingFace Transformers** (pure Python, no compilation)
- **External API** (OpenAI, Anthropic) - though this violates the "local only" requirement

See `src/generation/generator.py` for the current implementation.

---

**Quick Fix Command:**
```powershell
pip install --upgrade pip
pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu
```





