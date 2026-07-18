# Deployment Guide for Streamlit Cloud

## Step-by-Step Deployment to Streamlit Cloud

### 1. Get Your Groq API Key
- Go to: https://console.groq.com/keys
- Create/copy your API key
- Keep it safe (you'll need it in Step 5)

### 2. Push Latest Code to GitHub
Your code is already in the repo. Make sure all files are committed:
```bash
git add .
git commit -m "Add deployment configuration"
git push origin main
```

### 3. Go to Streamlit Cloud
- Visit: https://streamlit.io/cloud
- Sign in with your GitHub account (HARI7591)

### 4. Create New App
- Click **"New app"** button
- Fill in:
  - **GitHub repo**: HARI7591/Hari_AI
  - **Branch**: main
  - **Main file path**: app.py

### 5. Add Secret Environment Variable
- After app deploys (in 1-2 minutes), it may show an error
- Click **"Settings"** (⚙️ icon in top right)
- Go to **"Secrets"** tab
- Paste your secret:
```
GROQ_API_KEY=your_actual_groq_api_key_here
```
- Click **"Save"**
- The app will auto-reload

### 6. Done! ✅
Your app is now live and accessible via a public URL!

---

## If You Get an Error

**Error: "ModuleNotFoundError: No module named 'src'"**
- ✅ Already fixed - we created the `src` folder with all modules

**Error: "GROQ_API_KEY not found"**
- Go to Streamlit Settings → Secrets
- Make sure you've added the API key
- Wait 10 seconds for reload

**Error: "Import Error for LangChain"**
- All dependencies are in `requirements.txt`
- Streamlit Cloud auto-installs them

---

## Troubleshooting

If the app still doesn't work:

1. Check the logs (click "Manage app" → "Logs")
2. Look for error messages
3. Common issues:
   - Groq API key not set → Add in Secrets
   - Missing modules → All are in requirements.txt
   - Python version → Should be 3.11 (default on Streamlit Cloud)

---

## Alternative: Test Locally First

```bash
# Create virtual environment
python -m venv venv

# Activate
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

# Install
pip install -r requirements.txt

# Create .env file with
echo GROQ_API_KEY=your_key_here > .env

# Run
streamlit run app.py
```

Then access: http://localhost:8501

---

**That's it! Streamlit Cloud handles everything else automatically.** 🚀
