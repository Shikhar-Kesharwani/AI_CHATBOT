# ╔══════════════════════════════════════════════════════════════════════════╗
# ║     UNIVERSAL DUAL ARCHITECTURE DEPLOYMENT PROMPT v2.0                 ║
# ║     Created from: Adaptive RAG Agentic AI Chatbot Project              ║
# ║     Battle-tested, 100% Free, Production-Grade Deployment Guide        ║
# ╚══════════════════════════════════════════════════════════════════════════╝

Paste this entire document at the start of any new project's deployment phase.
It instructs an AI coding assistant to scaffold and execute both deployment
architectures from one codebase — without touching application logic, UI, or features.

---

## IDENTITY OF THIS PROMPT

This is the **Universal Dual Architecture Deployment Prompt (UDADP) v2.0**.
Battle-tested on a real production Python AI/ML project (FastAPI + Streamlit + FAISS + LangGraph).

It governs **two fully independent deployment tracks** for any project:

| Track | Name | Purpose |
|---|---|---|
| **Model 1** | Cloud-Native (Managed, Free) | Public live link for demos, portfolios, interviews |
| **Model 2** | Self-Hosted Docker Compose | Runs identically on any machine, OS, or VPS |

Both models run from the **same source code** with **zero changes** to application logic.

---

## ABSOLUTE GOVERNING RULES (READ FIRST — OVERRIDE EVERYTHING ELSE)

1. **Preservation First.** The application must look, feel, and behave exactly as
   it does on localhost after deployment. Do NOT modify any UI, UX, page layout,
   styling, business logic, API contract, feature, or route.

2. **Additive Only.** All deployment work adds new config files alongside the
   application code — never inside it. Never reorganize `src/`.

3. **If a code change is unavoidable** (e.g., hardcoded `localhost` URL must become
   an environment variable), follow this mandatory procedure:
   - State exactly what the change is.
   - State why it is required for production.
   - State the risk of making it.
   - State alternatives considered.
   - Make the **smallest possible backward-compatible change only**.

4. **Secrets never touch Git.** Only `.env.example` files (with placeholder values)
   are ever committed. All real credentials go into the hosting platform's secret
   manager or a gitignored `.env` file.

5. **Never break localhost.** After scaffolding both models, the developer must
   still be able to run the app exactly as before with zero new required setup steps.

6. **Everything free.** Never choose a service that requires a credit card, even
   for the "free tier". If a provider requires payment info, choose the next option.

---

## SECTION 1: PROJECT ANALYSIS PHASE

Before writing a single file, scan the project and identify:

1. Programming language and version (Python 3.x, Node.js 18, etc.)
2. Framework (Flask, FastAPI, Express, Next.js, Django, Streamlit, etc.)
3. Monolith or decoupled frontend/backend architecture
4. Entrypoint file(s)
5. Port(s) the application runs on
6. Whether it has ML/AI dependencies (LangChain, FAISS, transformers, etc.)
7. Whether it stores files/images/indexes locally
8. Whether it uses a database (SQL, NoSQL, vector, file-based)
9. Whether it has WebSocket requirements (Streamlit, real-time apps)

**Classify the deployment difficulty:**

| Class | Criteria | Model 1 Target |
|---|---|---|
| **Class A (Lightweight)** | No ML, RAM < 512MB, no WebSockets | Render Web Service or Vercel |
| **Class B (Stateful ML)** | FAISS/SQLite local files, WebSockets, LangGraph | Render (Docker) + persistent disk |
| **Class C (Heavy ML)** | TensorFlow/PyTorch model weights > 500MB | Hugging Face Spaces (Docker, 16GB RAM free) |

**Report findings to the user before writing any file.**

---

## SECTION 2: REPOSITORY STRUCTURE TO SCAFFOLD

Create this structure without moving any existing source files:

```
project-root/
├── infra/
│   ├── cloud/
│   │   ├── DEPLOYMENT_GUIDE.md     ← Step-by-step instructions for all options
│   │   └── render.yaml             ← Render Blueprint / Web Service config
│   └── docker/
│       ├── docker-compose.yml      ← Full self-hosted stack
│       ├── docker-compose.prod.yml ← Production resource limits and overrides
│       ├── nginx/
│       │   └── default.conf        ← Nginx reverse proxy (with WebSocket support)
│       └── .env.example            ← Docker-specific env vars template
├── .github/
│   └── workflows/
│       ├── ci.yml                  ← Build Docker image + health check
│       ├── lint.yml                ← Code quality (ruff for Python)
│       ├── test.yml                ← Run pytest if tests/ exists
│       ├── security.yml            ← pip-audit CVE scan + Gitleaks secret scan
│       ├── release.yml             ← Auto GitHub Release on version tag
│       └── deploy.yml              ← Trigger Render deploy hook on push to main
├── docs/
│   ├── ARCHITECTURE.md             ← Mermaid diagrams of both models
│   ├── DEPLOYMENT.md               ← Combined deployment reference
│   └── TROUBLESHOOTING.md          ← Common issues and fixes
├── Dockerfile                      ← Root-level, works on ALL platforms
├── supervisord.conf                ← (Only if running 2 processes in 1 container)
├── .env.example                    ← Root-level env var reference
└── .gitignore                      ← Hardened to block all secrets and artifacts
```

---

## SECTION 3: FREE TIER PROVIDER SELECTION ENGINE

### 3.1 The Golden Rule on "Free"
**A service is only FREE if it requires NO credit card to sign up and use the free tier.**
Never use Vercel Serverless, Google Cloud Run, AWS, Azure, or any platform that
requires payment information upfront for "free" access.

### 3.2 Backend / Compute

| Priority | Platform | Free Tier | Credit Card? | Best For |
|---|---|---|---|---|
| **1st** | **Render Web Service** | 750 hrs/month, Docker support | ❌ No | APIs, full-stack, Python, WebSockets |
| **2nd** | **Hugging Face Spaces (Docker)** | 16GB RAM, 2 vCPU, always-on | ❌ No | Heavy ML models, large apps |
| **3rd** | **Railway** | $5 credit/month | ❌ No | Node.js, quick deploys |

**Critical:** Never deploy Streamlit to Vercel. Vercel is serverless and drops
WebSocket connections after 10 seconds. Streamlit requires persistent WebSockets.

### 3.3 Frontend

| Priority | Platform | Free Tier | Credit Card? | Best For |
|---|---|---|---|---|
| **1st** | **Streamlit Community Cloud** | Unlimited public apps | ❌ No | Streamlit ONLY |
| **2nd** | **Vercel** | Generous free tier | ❌ No | React, Next.js, static sites |
| **3rd** | **Cloudflare Pages** | Unlimited bandwidth | ❌ No | Static sites, SPAs |
| **Avoid** | Vercel for Streamlit | Will crash | N/A | WebSocket incompatible |

### 3.4 Database

| Priority | Platform | Free Tier | Credit Card? | Best For |
|---|---|---|---|---|
| **1st** | **SQLite (local file)** | Free forever | ❌ No | Chat history, sessions, small data |
| **2nd** | **Neon** | 0.5GB Postgres | ❌ No | SQL apps needing real Postgres |
| **3rd** | **Supabase** | 500MB + Auth + Storage | ❌ No | Auth + DB + realtime |
| **Avoid** | CockroachDB | Needs credit card | ✅ Yes | Don't use for portfolio |

**Critical rule:** Never switch from SQLite to Postgres just to "look more production".
Switching databases changes application functionality and violates the preservation rule.
Only migrate if the application genuinely requires Postgres features.

### 3.5 Vector Store / ML Index

| Priority | Platform | Free Tier | Credit Card? | Best For |
|---|---|---|---|---|
| **1st** | **FAISS (local file)** | Free forever | ❌ No | Document search, RAG |
| **2nd** | **Pinecone** | 1 index, 100K vectors | ❌ No | Production vector search |
| **3rd** | **Weaviate Cloud** | 14-day sandbox | ❌ No | Graph + vector hybrid |

### 3.6 Object Storage

| Priority | Platform | Free Tier | Credit Card? | Best For |
|---|---|---|---|---|
| **1st** | **MinIO (self-hosted in Docker)** | Free forever | ❌ No | Model 2 local storage |
| **2nd** | **Cloudflare R2** | 10GB/month | ✅ Yes (avoid) | If budget allows |
| **3rd** | **Supabase Storage** | 1GB | ❌ No | If using Supabase already |

### 3.7 CI/CD

**Always use GitHub Actions** — 2000 minutes/month free, zero credit card needed.

### 3.8 Error Monitoring

**Sentry** — 5,000 errors/month free, zero credit card, one-line SDK integration.
Only activates when `SENTRY_DSN` environment variable is set — safe to include
in code without forcing anyone to use it.

---

## SECTION 4: MODEL 1 — CLOUD-NATIVE DEPLOYMENT

### 4.1 Dockerfile (Universal — Works on Render, Hugging Face, Railway)

```dockerfile
FROM python:3.10-slim

# ── System Dependencies ──────────────────────────────────────────────────────
# supervisor is used to run multiple processes (e.g., FastAPI + Streamlit)
RUN apt-get update && apt-get install -y --no-install-recommends \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# ── Non-Root User (Required by HuggingFace, good practice everywhere) ────────
RUN useradd -m -u 1000 user
USER user

ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

# ── Dependencies (before copying source for better layer caching) ────────────
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Application Code ─────────────────────────────────────────────────────────
COPY --chown=user . .

# ── Ports ────────────────────────────────────────────────────────────────────
# PORT env var is injected by the hosting platform
# 7860 = Hugging Face Spaces default
# 10000 = Render default
# 8501 = Streamlit standard
EXPOSE 8000 7860 8501 10000

# ── Startup ──────────────────────────────────────────────────────────────────
CMD ["supervisord", "-c", "supervisord.conf"]
```

### 4.2 supervisord.conf (For projects with 2 processes: API + Frontend)

Only needed when running both a backend API and a Streamlit frontend in one container.

```ini
[supervisord]
nodaemon=true
logfile=/dev/null
logfile_maxbytes=0

# Backend API starts first (priority=1)
[program:api]
command=python -m uvicorn src.main:app --host 0.0.0.0 --port 8000
autostart=true
autorestart=true
startsecs=5
priority=1
stdout_logfile=/dev/stdout
stdout_logfile_maxbytes=0
stderr_logfile=/dev/stderr
stderr_logfile_maxbytes=0

# Frontend starts after API (priority=2, reads PORT from env)
[program:streamlit]
command=python -m streamlit run streamlit_app/home.py --server.port=%(ENV_PORT)s --server.address=0.0.0.0 --server.headless=true
autostart=true
autorestart=true
startsecs=8
priority=2
stdout_logfile=/dev/stdout
stdout_logfile_maxbytes=0
stderr_logfile=/dev/stderr
stderr_logfile_maxbytes=0
```

### 4.3 render.yaml (Render Blueprint — One-Click Deploy)

```yaml
services:
  - type: web
    name: your-app-name
    env: docker
    dockerfilePath: ./Dockerfile
    envVars:
      - key: PORT
        value: 10000
      - key: API_URL
        value: http://localhost:8000
      - key: SQLITE_DB_PATH
        value: /data/app.db
      - key: ALLOWED_ORIGINS
        value: https://your-app-name.onrender.com
      - key: YOUR_API_KEY_1
        sync: false    # Set manually in Render dashboard → Secret
      - key: YOUR_API_KEY_2
        sync: false
      - key: SENTRY_DSN
        sync: false
    # Persistent disk keeps SQLite DB and any local files across restarts
    disk:
      name: app-data
      mountPath: /data
      sizeGB: 1
    healthCheckPath: /health
```

### 4.4 Render Web Service Manual Setup (Step-by-Step)

```
1. Go to dashboard.render.com → New + → Web Service
2. Connect GitHub repo → Select your repository
3. Fill in:
   - Name:        your-app-name
   - Language:    Docker  ← CRITICAL: Select Docker, not Python
   - Branch:      main
   - Region:      Oregon (US West)  ← or closest to you
   - Instance:    Free ($0/month)
4. Environment Variables → Add Variable:
   - PORT = 10000
   - API_URL = http://localhost:8000
   - [Your actual API keys]
5. Advanced → Disks → Add Disk:
   - Name: app-disk
   - Mount Path: /data
   - Size: 1 GB
6. Click Create Web Service
7. Wait 5-10 minutes for build
8. Your live URL appears at top-left of the Render dashboard
```

### 4.5 Hugging Face Spaces Setup (For Class C — Heavy ML)

```
1. huggingface.co → New Space
2. SDK: Docker → Blank
3. Hardware: Free (2 vCPU, 16GB RAM)
4. Visibility: Public
5. Push code:
   git remote add hf https://huggingface.co/spaces/[username]/[space-name]
   git push hf main
6. Settings → Variables and Secrets:
   PORT = 7860
   [Your API keys]
7. Live URL: https://[username]-[space-name].hf.space
```

---

## SECTION 5: MODEL 2 — SELF-HOSTED DOCKER COMPOSE

### 5.1 docker-compose.yml

```yaml
version: '3.9'

services:

  # ── Application (API + Frontend via Supervisord) ────────────────────────
  app:
    build:
      context: ../../
      dockerfile: Dockerfile
    container_name: app
    restart: unless-stopped
    environment:
      - PORT=8501
      - API_URL=http://localhost:8000
      - SQLITE_DB_PATH=/data/app.db
      - ALLOWED_ORIGINS=http://localhost,http://localhost:8501
      - YOUR_API_KEY_1=${YOUR_API_KEY_1}
      - YOUR_API_KEY_2=${YOUR_API_KEY_2}
      - SENTRY_DSN=${SENTRY_DSN:-}
    volumes:
      - app_data:/data          # Persistent SQLite DB + any local indexes
      - app_logs:/home/user/app/logs
    depends_on:
      minio:
        condition: service_started
    networks:
      - app_network
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:8000/health || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 20s

  # ── Object Storage (MinIO — Self-Hosted S3) ────────────────────────────
  minio:
    image: minio/minio:latest
    container_name: minio
    restart: unless-stopped
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: ${MINIO_ROOT_USER:-minioadmin}
      MINIO_ROOT_PASSWORD: ${MINIO_ROOT_PASSWORD:-minioadmin123}
    volumes:
      - minio_data:/data
    ports:
      - "9000:9000"    # S3 API
      - "9001:9001"    # MinIO Console
    networks:
      - app_network

  # ── Reverse Proxy (Nginx with WebSocket support) ────────────────────────
  nginx:
    image: nginx:alpine
    container_name: nginx
    restart: unless-stopped
    ports:
      - "80:80"
    volumes:
      - ./nginx/default.conf:/etc/nginx/conf.d/default.conf:ro
    depends_on:
      - app
    networks:
      - app_network

volumes:
  app_data:
  minio_data:
  app_logs:

networks:
  app_network:
    driver: bridge
```

### 5.2 docker-compose.prod.yml (Production Overrides)

```yaml
version: '3.9'

services:
  app:
    restart: always
    environment:
      - DEBUG=False
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 2G

  nginx:
    restart: always
    ports:
      - "80:80"
      - "443:443"

  minio:
    restart: always
```

### 5.3 nginx/default.conf (With Full WebSocket Support)

```nginx
server {
    listen 80;
    server_name _;

    # ── Frontend (Streamlit) ──────────────────────────────────────────────
    location / {
        proxy_pass http://app:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket support — REQUIRED by Streamlit
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_read_timeout 86400;
    }

    # ── Backend API ───────────────────────────────────────────────────────
    location /api/ {
        rewrite ^/api/(.*) /$1 break;
        proxy_pass http://app:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # ── Health check ──────────────────────────────────────────────────────
    location /health {
        proxy_pass http://app:8000/health;
    }

    # ── Upload limit ──────────────────────────────────────────────────────
    client_max_body_size 50M;
}
```

### 5.4 Docker Compose Launch Commands

```bash
# Copy env template and fill in your secrets
cp infra/docker/.env.example infra/docker/.env

# Development
docker-compose -f infra/docker/docker-compose.yml up -d

# Production (with resource limits)
docker-compose -f infra/docker/docker-compose.yml \
               -f infra/docker/docker-compose.prod.yml up -d

# View logs
docker-compose -f infra/docker/docker-compose.yml logs -f

# Stop all
docker-compose -f infra/docker/docker-compose.yml down
```

---

## SECTION 6: APPLICATION CODE REQUIREMENTS

### 6.1 Health Check Endpoints (REQUIRED for Render + Docker healthchecks)

Add these 3 endpoints to your main API file:

```python
import time
_start_time = time.time()

@app.get("/health")
async def health():
    return {"status": "ok", "uptime_seconds": round(time.time() - _start_time, 2)}

@app.get("/ready")
async def ready():
    return {"status": "ready"}

@app.get("/live")
async def live():
    return {"status": "alive"}
```

### 6.2 CORS Middleware (REQUIRED for decoupled frontend/backend)

```python
import os
from fastapi.middleware.cors import CORSMiddleware

allowed_origins = os.environ.get(
    "ALLOWED_ORIGINS",
    "http://localhost:8501,http://localhost:3000,http://127.0.0.1:8501"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
)
```

### 6.3 Sentry Error Monitoring (OPTIONAL — zero-cost)

```python
import os
_sentry_dsn = os.environ.get("SENTRY_DSN", "")
if _sentry_dsn:
    import sentry_sdk
    sentry_sdk.init(dsn=_sentry_dsn, traces_sample_rate=0.2)
```

### 6.4 Environment-Aware Configuration (REQUIRED for any hardcoded paths)

```python
# API URL (for frontend → backend communication)
API_URL = os.environ.get("API_URL", "http://127.0.0.1:8000")

# Database path
DB_PATH = os.environ.get("DB_PATH", "app.db")

# Local file storage (FAISS index, uploaded files, etc.)
STORAGE_DIR = os.environ.get("STORAGE_DIR", "local_storage")
```

---

## SECTION 7: GITHUB ACTIONS WORKFLOWS (ALL 6 — COPY-PASTE READY)

### ci.yml
```yaml
name: CI — Build & Health Check
on:
  push: {branches: [main, develop]}
  pull_request: {branches: [main]}
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build Docker image
        run: docker build -t app:ci .
      - name: Start and health check
        run: |
          docker run -d --name ci_app -p 8000:8000 \
            -e PORT=8000 -e API_URL=http://localhost:8000 \
            app:ci
          sleep 25
          curl -f http://localhost:8000/health || (docker logs ci_app && exit 1)
      - name: Cleanup
        if: always()
        run: docker rm -f ci_app
```

### lint.yml
```yaml
name: Lint — Code Quality
on:
  push: {branches: [main, develop]}
  pull_request: {branches: [main]}
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: {python-version: "3.10"}
      - run: pip install ruff
      - run: ruff check src/ --output-format=github
      - run: ruff format src/ --check
```

### test.yml
```yaml
name: Test — Unit Tests
on:
  push: {branches: [main, develop]}
  pull_request: {branches: [main]}
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: {python-version: "3.10"}
      - run: pip install pytest pytest-asyncio httpx && pip install -r requirements.txt
      - run: |
          if [ -d "tests" ]; then pytest tests/ -v; else echo "No tests. Skipping."; fi
```

### security.yml
```yaml
name: Security — Dependency Scan
on:
  push: {branches: [main]}
  schedule:
    - cron: "0 9 * * 1"
jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: {python-version: "3.10"}
      - run: pip install pip-audit && pip-audit -r requirements.txt
      - uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### release.yml
```yaml
name: Release — Auto GitHub Release
on:
  push:
    tags: ["v*.*.*"]
jobs:
  release:
    runs-on: ubuntu-latest
    permissions: {contents: write}
    steps:
      - uses: actions/checkout@v4
      - uses: softprops/action-gh-release@v2
        with:
          generate_release_notes: true
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### deploy.yml
```yaml
name: Deploy — Trigger Render
on:
  push: {branches: [main]}
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Trigger Render Deploy Hook
        if: ${{ secrets.RENDER_DEPLOY_HOOK_URL != '' }}
        run: curl -X POST "${{ secrets.RENDER_DEPLOY_HOOK_URL }}"
```

---

## SECTION 8: .GITIGNORE HARDENING

Add these lines to your `.gitignore`:

```gitignore
# Environment files — NEVER commit secrets
.env
.env.*
!.env.example

# Local databases and indexes
*.db
*.sqlite
*.sqlite3
faiss_index_persistent/
local_storage/

# Model weights and large ML artifacts
*.h5
*.pkl
*.pt
*.pth
*.onnx
*.joblib
*.bin
data/
datasets/
Artifacts/
models/

# Docker secrets
infra/docker/.env

# Python
__pycache__/
*.pyc
venv/
.venv/
*.egg-info/

# Logs
*.log
```

---

## SECTION 9: ENVIRONMENT VARIABLES REFERENCE

### Root .env.example (commit this, not .env)
```env
# ── Required API Keys ────────────────────────────────
YOUR_API_KEY_1=your_key_here
YOUR_API_KEY_2=your_key_here

# ── Application Routing ──────────────────────────────
API_URL=http://localhost:8000
PORT=8501

# ── Database & Storage Paths ─────────────────────────
DB_PATH=app.db
STORAGE_DIR=local_storage

# ── CORS ─────────────────────────────────────────────
ALLOWED_ORIGINS=http://localhost,http://localhost:8501

# ── Monitoring (optional — get free DSN at sentry.io) ─
SENTRY_DSN=
```

---

## SECTION 10: DEPLOYMENT DECISION FLOWCHART

```
START
  │
  ├── Does the app use Streamlit?
  │     YES → Do NOT use Vercel. Use Render (Docker) or Streamlit Community Cloud.
  │     NO  → Vercel is fine for React/Next.js/static frontends.
  │
  ├── Does the app use ML models (FAISS, LangChain, transformers)?
  │     YES → Model weights exceed Vercel's 50MB limit. Use Render or Hugging Face.
  │     NO  → Any platform works.
  │
  ├── Does the app store files locally (SQLite, uploaded files)?
  │     YES → Add a Persistent Disk on Render (1GB free) or use Docker volumes.
  │     NO  → Stateless deployment works without persistent disk.
  │
  ├── Does the app have WebSocket requirements?
  │     YES → Use Render, Railway, or Hugging Face. NOT Vercel.
  │     NO  → Any platform works.
  │
  └── Is the ML model larger than 1GB?
        YES → Use Hugging Face Spaces (16GB RAM free, no credit card).
        NO  → Render free tier (512MB RAM) is sufficient.
```

---

## SECTION 11: POST-DEPLOYMENT CHECKLIST

### Model 1 (Cloud Native):
- [ ] Render service shows "Live" green badge
- [ ] `/health` endpoint returns `{"status": "ok"}`
- [ ] All app features work identically to localhost
- [ ] No secrets visible in GitHub repo or build logs
- [ ] GitHub Actions CI runs and passes on push to main

### Model 2 (Docker Compose):
- [ ] `docker-compose up -d` completes without errors
- [ ] Nginx accessible at `http://localhost`
- [ ] App healthcheck passes: `curl http://localhost/health`
- [ ] MinIO console accessible at `http://localhost:9001`
- [ ] Persistent volume survives `docker-compose restart`
- [ ] App works identically to running without Docker

---

## SECTION 12: COMMON MISTAKES TO AVOID

| ❌ Wrong | ✅ Right |
|---|---|
| Deploy Streamlit to Vercel | Deploy Streamlit to Render or Streamlit Cloud |
| Hardcode `localhost:8000` in frontend | Use `os.environ.get("API_URL", "http://localhost:8000")` |
| Switch SQLite to Postgres "to look professional" | Keep SQLite if app already uses it |
| Commit `.env` file | Only commit `.env.example` with placeholder values |
| Expose Nginx port 80 without WebSocket headers | Add `Upgrade` and `Connection` headers in Nginx |
| Use Google Cloud Run, AWS (credit card required) | Use Render, Hugging Face, Streamlit Cloud |
| Run container as root | Use `useradd -m -u 1000 user` in Dockerfile |
| Hardcode database/storage paths | Read paths from environment variables |
| Skip health check endpoints | Always add `/health`, `/ready`, `/live` |
| Start Streamlit before API is ready | Use `supervisord` `priority` and `startsecs` |

---

*UDADP v2.0 — Battle-tested on a real production Python AI/ML project.*
*100% free, zero credit cards, full feature parity on all platforms.*
