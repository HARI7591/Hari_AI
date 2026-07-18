# Complete Step-by-Step Setup Guide for Hari AI Career Coach

## Prerequisites
- Python 3.10, 3.11, or 3.12 installed
- VS Code installed
- Git installed
- Groq API key (get from https://console.groq.com/keys)

---

## Step 1: Open Project in VS Code

```bash
# Navigate to the project folder
cd path/to/Hari_AI

# Open in VS Code
code .
```

---

## Step 2: Create Virtual Environment

Open the **Terminal in VS Code** (Ctrl + `) and run:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# For Windows (PowerShell):
venv\Scripts\activate

# For Windows (Command Prompt):
venv\Scripts\activate.bat

# For Mac/Linux:
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

---

## Step 3: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt
```

This will install:
- Streamlit
- LangChain
- ChromaDB
- HuggingFace Embeddings
- Groq LLM
- PDF/DOCX readers
- And more...

**Wait for installation to complete** (may take 2-3 minutes)

---

## Step 4: Create .env File

In the project root, create a new file named `.env`:

```bash
# Method 1: Using VS Code
# Right-click in Explorer → New File → name it ".env"

# Method 2: Using Terminal
touch .env
```

Add this line to `.env`:

```
GROQ_API_KEY=your_actual_groq_api_key_here
```

Replace `your_actual_groq_api_key_here` with your real key from https://console.groq.com/keys

---

## Step 5: Verify Project Structure

Your folder should look like this:

```
Hari_AI/
├── app.py                 # Main Streamlit app
├── requirements.txt       # Dependencies
├── .env                   # Your API key (KEEP SECRET!)
├── .env.example          # Template (don't edit)
├── README.md
├── DEPLOYMENT.md
├── src/
│   ├── __init__.py
│   ├── file_utils.py     # File handling
│   ├── rag_engine.py     # RAG logic
├── .streamlit/
│   └── config.toml       # Streamlit config
└── (other folders)
```

**Important:** `.env` file should NEVER be pushed to GitHub (it's in `.gitignore`)

---

## Step 6: Test Locally

In terminal with `(venv)` activated, run:

```bash
streamlit run app.py
```

You should see:

```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

**Open the URL in your browser**

---

## Step 7: Test the App

1. **Paste sample resume** in the Resume text area:
```
John Doe
Senior Software Engineer
Python, Java, AWS, Docker
5 years experience in backend development
```

2. **Paste sample job description**:
```
Backend Engineer Role
Requirements: Python, Docker, Kubernetes, AWS
Experience: 3+ years
```

3. Click **"🚀 Build Career Coach RAG Index"**
4. Wait for completion
5. Click **"🤖 Get Career Coach Answer"**

If everything works → ✅ App is running correctly!

---

## Step 8: Stop the App

Press `Ctrl + C` in terminal to stop Streamlit

---

## Troubleshooting

### Error: "No module named 'src'"
**Solution:**
```bash
# Make sure you're in the right directory
pwd  # Should show path ending with "Hari_AI"

# Reinstall dependencies
pip install -r requirements.txt
```

### Error: "GROQ_API_KEY not found"
**Solution:**
1. Check `.env` file exists in project root
2. Verify format: `GROQ_API_KEY=your_key` (no spaces)
3. Restart Streamlit: `Ctrl + C` then `streamlit run app.py`

### Error: "ModuleNotFoundError"
**Solution:**
```bash
# Reinstall all packages
pip install --upgrade -r requirements.txt

# Or install individually
pip install streamlit langchain chromadb pypdf python-docx
```

### Error: "Port 8501 already in use"
**Solution:**
```bash
# Use different port
streamlit run app.py --server.port 8502
```

---

## Common Commands

```bash
# Activate virtual environment (do this every time)
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Run the app
streamlit run app.py

# Stop the app
Ctrl + C

# Deactivate virtual environment
deactivate

# Check installed packages
pip list

# Update a package
pip install --upgrade packagename

# Remove virtual environment (only if needed)
rm -r venv  # Mac/Linux
rmdir /s venv  # Windows
```

---

## Next Steps (After Local Testing)

Once the app works locally, deploy to Streamlit Cloud:

1. Push to GitHub:
```bash
git add .
git commit -m "Initial commit with all fixes"
git push origin main
```

2. Go to https://streamlit.io/cloud
3. Create new app
4. Select repo and app.py
5. Add GROQ_API_KEY in Secrets

---

## Need Help?

If you encounter errors:
1. Share the **exact error message**
2. Share the **command you ran**
3. Tell me **what happened**

Good luck! 🚀
