# 🚀 How to Run the App

## The Problem
You're getting "No module named streamlit" because the system Python is being used instead of the virtual environment.

## ✅ Solution: Use Virtual Environment Python

### Method 1: Use the Run Script (Easiest)

```powershell
.\run_app.ps1
```

### Method 2: Manual Activation

```powershell
# Step 1: Activate virtual environment
.\venv\Scripts\Activate.ps1

# Step 2: Run using venv Python
.\venv\Scripts\python.exe -m streamlit run app.py
```

### Method 3: Direct Path (No Activation Needed)

```powershell
.\venv\Scripts\python.exe -m streamlit run app.py
```

## 🔍 How to Check You're Using the Right Python

**Wrong (System Python):**
```
C:\Users\raksh\AppData\Local\Programs\Python\Python39\python.exe
```

**Correct (Virtual Environment):**
```
C:\Users\raksh\Desktop\rag-medical-qa\venv\Scripts\python.exe
```

## 💡 Quick Fix

Just run:
```powershell
.\venv\Scripts\python.exe -m streamlit run app.py
```

This uses the Python from your virtual environment where streamlit is installed.

## 📝 Why This Happens

- Your IDE/terminal might be using system Python
- Virtual environment needs to be activated
- Or use the full path to venv Python

---

**Try the run script: `.\run_app.ps1`**




