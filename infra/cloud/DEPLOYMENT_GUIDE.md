# Cloud Native Deployment Guide — Model 1
## Platform: Render (Backend) + Streamlit Community Cloud (Frontend)

> **Why these platforms?**
> - Both are **100% free** with no credit card required.
> - Render supports Docker containers and WebSockets — perfect for FastAPI.
> - Streamlit Community Cloud is Streamlit's official hosting platform with native WebSocket support.

---

## Option A: Deploy on Render (Full Stack — Recommended for demos)

This deploys BOTH FastAPI and Streamlit inside one Docker container via Render.
You get a single URL for everything.

### Step 1: Push your code to GitHub
Ensure your latest code is on `main`:
```bash
git push origin main
```

### Step 2: Create a Render account
Go to [render.com](https://render.com) → Sign up (no credit card needed).

### Step 3: Deploy via Blueprint (Automatic)
1. In Render dashboard → **New** → **Blueprint**
2. Connect your GitHub repo: `AyushGU12/AI_CHATBOT`
3. Render will auto-detect `infra/cloud/render.yaml` and configure everything.

### Step 4: Set Secret Environment Variables
In your Render service → **Environment** tab, add:
```
OPENAI_API_KEY   = <your actual OpenAI key>
TAVILY_API_KEY   = <your actual Tavily key>
SENTRY_DSN       = <optional — your Sentry DSN>
```

### Step 5: Deploy
Click **Save and Deploy**. Your app will be live at:
```
https://adaptive-rag.onrender.com
```

> **Note:** Free tier services spin down after 15 minutes of inactivity.
> First request after idle takes ~30 seconds (cold start). This is expected.

---

## Option B: Deploy on Streamlit Community Cloud (Frontend Only)

Use this if you want a dedicated Streamlit URL that people can share easily.

### Step 1: Create a Streamlit account
Go to [share.streamlit.io](https://share.streamlit.io) → Sign up with GitHub (free, no credit card).

### Step 2: Create a new App
1. **Repository:** `AyushGU12/AI_CHATBOT`
2. **Branch:** `main`
3. **Main file:** `streamlit_app/home.py`

### Step 3: Set Secrets
In Streamlit Cloud → **App Settings** → **Secrets**, paste:
```toml
API_URL = "https://adaptive-rag.onrender.com"
OPENAI_API_KEY = "your_openai_key"
TAVILY_API_KEY = "your_tavily_key"
```

### Step 4: Deploy
Click **Deploy**. Your frontend will be live at:
```
https://[username]-ai-chatbot-[hash].streamlit.app
```

---

## Option C: Deploy on Hugging Face Spaces (Original — ML Demo)

Use this if you want the app on Hugging Face's platform (16GB RAM free).

### Step 1: Create a Space
1. Go to [huggingface.co](https://huggingface.co) → New Space
2. **Space Name:** adaptive-rag-chatbot
3. **SDK:** Docker → Blank
4. **Hardware:** Free (2 vCPU, 16GB RAM)
5. **Visibility:** Public

### Step 2: Push your code
```bash
git remote add hf https://huggingface.co/spaces/[username]/adaptive-rag-chatbot
git push hf main
```

### Step 3: Set Secrets
In your Space → **Settings** → **Variables and Secrets**:
```
PORT             = 7860
OPENAI_API_KEY   = <your key>
TAVILY_API_KEY   = <your key>
API_URL          = http://localhost:8000
```

### Step 4: Wait for build (~5 minutes)
Your app will be live at:
```
https://[username]-adaptive-rag-chatbot.hf.space
```

---

## Environment Variables Reference

| Variable | Required | Description |
|---|---|---|
| `OPENAI_API_KEY` | ✅ Yes | OpenAI API key for LLM |
| `TAVILY_API_KEY` | ✅ Yes | Tavily key for web search |
| `API_URL` | ✅ Yes | URL of FastAPI backend |
| `PORT` | Platform | Set by platform automatically |
| `SQLITE_DB_PATH` | Optional | Override SQLite path |
| `FAISS_INDEX_DIR` | Optional | Override FAISS index path |
| `ALLOWED_ORIGINS` | Optional | CORS origins for production |
| `SENTRY_DSN` | Optional | Sentry error monitoring |
