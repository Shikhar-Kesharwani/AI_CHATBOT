# ╔══════════════════════════════════════════════════════════════════════════╗
# ║   UNIVERSAL DUAL ARCHITECTURE DEPLOYMENT PROMPT v3.0                   ║
# ║   Truly Universal — Works for ANY tech stack, ANY language              ║
# ║   React · Next.js · Node · Flask · FastAPI · Django · Streamlit        ║
# ║   Vue · Svelte · Express · Spring · Rails · Laravel · Go · Rust        ║
# ╚══════════════════════════════════════════════════════════════════════════╝

Paste this entire document at the start of ANY project's deployment phase.
An AI coding assistant will analyze YOUR specific project and automatically
select the correct platforms, configs, and files for YOUR exact tech stack.
Nothing here is hardcoded to one framework or language.

---

## WHO THIS IS FOR

- Solo developers deploying portfolio projects
- Students deploying final-year projects
- Anyone who wants a permanent free live link + a one-command local setup
- Any AI coding assistant given a project to "productionize"

---

## ABSOLUTE GOVERNING RULES (OVERRIDE EVERYTHING ELSE)

1. **Preservation First.** The app must look, feel, and behave exactly as it
   does on localhost after deployment. Never touch UI, UX, business logic,
   API contracts, routes, or features.

2. **Additive Only.** All deployment work adds new files alongside the app.
   Never reorganize `src/`, never rename existing files.

3. **If a code change is unavoidable** (e.g., hardcoded `localhost` URL):
   - State exactly what the change is
   - State why production requires it
   - State the risk
   - State alternatives
   - Make the **smallest possible backward-compatible change only**

4. **Secrets never touch Git.** Only `.env.example` with placeholder values
   is ever committed. Real credentials go into the platform's secret manager.

5. **Never break localhost.** After deployment scaffolding, the developer must
   still run the app exactly as before with zero new setup steps.

6. **100% Free only.** Never choose any service requiring a credit card,
   even for "free tier" access. If a platform requires payment info, skip it.

---

## STEP 1 — PROJECT ANALYSIS (DO THIS BEFORE WRITING ANY FILE)

Scan the project and answer every question below. Report findings to the user
before touching anything.

### 1.1 Language & Runtime
```
- What language? (Python / JavaScript / TypeScript / Go / Java / Ruby / PHP / Rust / other)
- What version? (Python 3.10, Node 18, Go 1.21, etc.)
- What package manager? (pip / npm / yarn / pnpm / cargo / maven / composer)
```

### 1.2 Framework Detection
```
FRONTEND frameworks:
- React (Vite / CRA)       → Static build → Vercel / Cloudflare Pages
- Next.js                  → SSR or Static → Vercel (best fit)
- Vue / Nuxt               → Static or SSR → Vercel / Cloudflare Pages
- Svelte / SvelteKit       → Static or SSR → Vercel / Cloudflare Pages
- Streamlit                → Python persistent WebSocket → Render / HuggingFace
- Gradio                   → Python persistent WebSocket → HuggingFace Spaces
- HTML/CSS/JS (static)     → Static → GitHub Pages / Cloudflare Pages

BACKEND frameworks:
- FastAPI / Flask / Django → Python → Render (Docker or Python runtime)
- Express / Koa / Hapi     → Node.js → Render / Railway
- Next.js API Routes       → Serverless → Vercel
- Spring Boot              → Java → Render (Docker)
- Rails                    → Ruby → Render
- Laravel                  → PHP → Render (Docker)
- Go (net/http / Gin / Fiber) → Go → Render / Railway

FULL STACK (combined):
- Next.js (frontend + API) → Vercel (handles both natively)
- Remix                    → Vercel / Cloudflare Pages
- SvelteKit                → Vercel / Cloudflare Pages
- T3 Stack                 → Vercel
```

### 1.3 Architecture Type
```
- MONOLITH: Single app handles both frontend and backend
  (Next.js, Django with templates, Rails, Laravel)
  → Deploy as ONE service

- DECOUPLED: Separate frontend and backend repos/folders
  (React + FastAPI, Vue + Express, Streamlit + FastAPI)
  → Deploy as TWO independent services
  → Frontend talks to backend via API_URL env var

- MULTI-SERVICE: Multiple backend services
  → Deploy each service separately
```

### 1.4 Database Detection
```
- No database            → No DB deployment needed
- SQLite (file-based)    → Persistent disk on Render, Docker volume locally
- PostgreSQL             → Neon (free, no credit card)
- MySQL                  → PlanetScale free tier or Railway
- MongoDB                → MongoDB Atlas free tier (no credit card)
- Redis                  → Upstash Redis (no credit card)
- Vector DB (FAISS local)→ Persistent disk, keep as-is
- Vector DB (Pinecone)   → Pinecone free tier (no credit card)
```

### 1.5 Storage Detection
```
- No file uploads        → No storage service needed
- Local file storage     → Docker volume (Model 2) / Render disk (Model 1)
- Image/PDF uploads      → MinIO in Docker, Supabase Storage in cloud
```

### 1.6 Special Dependency Detection
```
- WebSockets required?     → Never use Vercel serverless for backend
- ML model files (>.pkl/.pt/.h5)? → Use HuggingFace Spaces (16GB RAM free)
- Background workers?      → Need always-on server, not serverless
- Cron jobs?               → GitHub Actions scheduled workflow
- Authentication?          → Supabase Auth (free) or JWT (self-managed)
- Long-running processes?  → Render or HuggingFace, NOT Vercel
```

### 1.7 Classify Deployment Difficulty

| Class | Criteria | Model 1 Target |
|---|---|---|
| **A — Static** | HTML/CSS/JS, no server, no DB | GitHub Pages or Cloudflare Pages |
| **B — Lightweight API** | Node/Python API, < 512MB RAM, no ML | Render (Python/Node runtime) |
| **C — Full Stack** | Decoupled frontend + backend | Vercel (frontend) + Render (backend) |
| **D — Stateful ML** | FAISS/SQLite local files, WebSockets | Render (Docker) with persistent disk |
| **E — Heavy ML** | Model weights > 500MB, needs GPU RAM | HuggingFace Spaces (Docker, 16GB free) |
| **F — Monolith SSR** | Next.js, Remix, SvelteKit | Vercel (native support) |

---

## STEP 2 — PROVIDER SELECTION ENGINE

### 2.1 Golden Rules
- A service is only "free" if it requires **NO credit card** to sign up.
- Always pick the highest-priority option that fits the project's class.
- If a provider later removes its free tier, automatically use the next option.

### 2.2 Frontend Hosting

| Priority | Platform | Free | No CC | Best For |
|---|---|---|---|---|
| 1 | **Vercel** | ✅ | ✅ | Next.js, React, Vue, SvelteKit, SSR |
| 2 | **Cloudflare Pages** | ✅ | ✅ | Static sites, SPAs |
| 3 | **GitHub Pages** | ✅ | ✅ | Pure static HTML/CSS/JS |
| 4 | **Streamlit Community Cloud** | ✅ | ✅ | Streamlit ONLY |
| 5 | **HuggingFace Spaces (Gradio)** | ✅ | ✅ | Gradio / Streamlit + ML |
| ❌ | Vercel for Streamlit/Gradio | Incompatible | — | Drops WebSockets |
| ❌ | Netlify (backend functions) | Limited | — | Use Render instead |

### 2.3 Backend / API Hosting

| Priority | Platform | Free | No CC | Best For |
|---|---|---|---|---|
| 1 | **Render Web Service** | ✅ | ✅ | Any Docker container, Python, Node |
| 2 | **HuggingFace Spaces (Docker)** | ✅ | ✅ | ML-heavy apps, 16GB RAM |
| 3 | **Railway** | ✅ | ✅ | Node.js, quick deploys ($5 credit) |
| 4 | **Fly.io** | ✅ | ✅ | Go, Rust, Docker |
| ❌ | Vercel Serverless Functions | 10s timeout | — | Too short for AI/ML |
| ❌ | Google Cloud Run | Requires CC | — | Credit card needed |
| ❌ | AWS / Azure | Requires CC | — | Credit card needed |

### 2.4 Database

| Priority | Platform | Free | No CC | Best For |
|---|---|---|---|---|
| 1 | **SQLite (keep as-is)** | ✅ | ✅ | Already in use — never migrate |
| 2 | **Neon** | ✅ | ✅ | PostgreSQL, serverless |
| 3 | **Supabase** | ✅ | ✅ | PostgreSQL + Auth + Storage |
| 4 | **MongoDB Atlas** | ✅ | ✅ | MongoDB, 512MB free |
| 5 | **PlanetScale** | ✅ | ✅ | MySQL compatible |
| 6 | **Upstash Redis** | ✅ | ✅ | Redis, caching, queues |
| ❌ | CockroachDB | Requires CC | — | Skip for portfolio |
| ❌ | Firebase | Requires CC | — | Skip unless already in use |

**Critical rule:** If the app already uses SQLite, NEVER migrate to PostgreSQL
just to "look professional". SQLite works perfectly in production with a
persistent disk. Migration = changing functionality = violation of Rule 1.

### 2.5 Object / File Storage

| Priority | Platform | Free | No CC | Best For |
|---|---|---|---|---|
| 1 | **Local disk / Docker volume** | ✅ | ✅ | Model 2 (self-hosted) |
| 2 | **Render Persistent Disk** | ✅ | ✅ | Model 1 (cloud), 1GB |
| 3 | **Supabase Storage** | ✅ | ✅ | 1GB, if using Supabase |
| 4 | **Cloudflare R2** | Limited | ✅* | 10GB, needs account |
| ❌ | AWS S3 | Requires CC | — | Use R2 instead |

### 2.6 CI/CD
**Always use GitHub Actions** — 2000 min/month free, no credit card, universal.

### 2.7 Error Monitoring
**Sentry** — 5,000 errors/month free, no credit card.
Integrate with one line. Only activates when `SENTRY_DSN` env var is set.

---

## STEP 3 — ARCHITECTURE DECISION OUTPUT

Based on Step 1 analysis, output the selected architecture in this format:

```
┌─────────────────────────────────────────────────────────────────┐
│  PROJECT:    [Project Name]                                     │
│  CLASS:      [A/B/C/D/E/F] — [Class Name]                      │
│  LANGUAGE:   [Language + Version]                               │
│  FRAMEWORK:  [Framework]                                        │
│  ARCH TYPE:  [Monolith / Decoupled / Multi-Service]             │
├─────────────────────────────────────────────────────────────────┤
│  MODEL 1 (Cloud Native):                                        │
│    Frontend:  [Platform + URL pattern]                          │
│    Backend:   [Platform + URL pattern]                          │
│    Database:  [Service or "Local SQLite on Render disk"]        │
│    Storage:   [Service or "Render disk" or "None needed"]       │
│    CI/CD:     GitHub Actions                                     │
├─────────────────────────────────────────────────────────────────┤
│  MODEL 2 (Self-Hosted Docker Compose):                          │
│    App:       [Description of services]                         │
│    Proxy:     Nginx                                             │
│    Storage:   Docker Named Volumes                              │
│    Command:   docker-compose -f infra/docker/docker-compose.yml up -d │
└─────────────────────────────────────────────────────────────────┘
```

---

## STEP 4 — REPOSITORY STRUCTURE TO SCAFFOLD

Add these files to the project. Do NOT move or rename any existing source files.

```
project-root/
├── infra/
│   ├── cloud/
│   │   ├── DEPLOYMENT_GUIDE.md    ← Step-by-step for this project's platforms
│   │   └── [platform].yaml        ← render.yaml / vercel.json / etc.
│   └── docker/
│       ├── docker-compose.yml     ← Full self-hosted stack
│       ├── docker-compose.prod.yml← Production resource limits
│       ├── nginx/
│       │   └── default.conf       ← Proxy config (with WebSocket if needed)
│       └── .env.example           ← Docker env vars template
├── .github/
│   └── workflows/
│       ├── ci.yml                 ← Build + health check on every push
│       ├── lint.yml               ← Code quality (eslint / ruff / golint)
│       ├── test.yml               ← Run tests if they exist
│       ├── security.yml           ← Dependency CVE scan weekly
│       ├── release.yml            ← Auto GitHub Release on version tag
│       └── deploy.yml             ← Trigger platform deploy on push to main
├── docs/
│   ├── ARCHITECTURE.md            ← Mermaid diagrams of both models
│   └── TROUBLESHOOTING.md         ← Common issues and fixes
├── Dockerfile                     ← Root level, works on all platforms
├── .env.example                   ← Root env var reference (committed)
└── .gitignore                     ← Hardened to block secrets + artifacts
```

---

## STEP 5 — DOCKERFILE TEMPLATES (SELECT ONE BY PROJECT TYPE)

### Template A: Python (FastAPI / Flask / Django — Backend Only)
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE ${PORT:-8000}
CMD ["sh", "-c", "python -m uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
```

### Template B: Python (Streamlit / Gradio — Frontend + Backend Combined)
```dockerfile
FROM python:3.10-slim

RUN apt-get update && apt-get install -y --no-install-recommends supervisor \
    && rm -rf /var/lib/apt/lists/*

# Non-root user (required by HuggingFace, good practice everywhere)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user PATH=/home/user/.local/bin:$PATH
WORKDIR $HOME/app

COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY --chown=user . .

# Expose all possible ports
# PORT env var is set by the hosting platform
EXPOSE 8000 7860 8501 10000

# supervisord.conf runs both API + frontend simultaneously
CMD ["supervisord", "-c", "supervisord.conf"]
```

### Template C: Node.js (Express / Koa / Hapi — Backend Only)
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json .
RUN npm ci --only=production
COPY . .
EXPOSE ${PORT:-3000}
CMD ["node", "server.js"]
```

### Template D: Node.js (Next.js — Full Stack Monolith)
```dockerfile
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json .
RUN npm ci
COPY . .
RUN npm run build

FROM node:18-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json
EXPOSE ${PORT:-3000}
CMD ["npm", "start"]
```

### Template E: React / Vue / Svelte (Static Frontend — Served by Nginx)
```dockerfile
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json .
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY infra/docker/nginx/default.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Template F: Go
```dockerfile
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY go.mod go.sum .
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o app .

FROM alpine:latest
WORKDIR /app
COPY --from=builder /app/app .
EXPOSE ${PORT:-8080}
CMD ["./app"]
```

---

## STEP 6 — SUPERVISORD TEMPLATE (ONLY FOR PYTHON DUAL-PROCESS)

Only needed when running a Python API backend AND a Streamlit/Gradio frontend
in the same container. Skip this for all other project types.

```ini
[supervisord]
nodaemon=true
logfile=/dev/null
logfile_maxbytes=0

# Backend starts first (priority=1, startsecs gives it time to boot)
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

# Frontend starts after API is ready (priority=2)
# %(ENV_PORT)s reads the PORT environment variable from the platform
[program:frontend]
command=python -m streamlit run app/main.py --server.port=%(ENV_PORT)s --server.address=0.0.0.0 --server.headless=true
autostart=true
autorestart=true
startsecs=8
priority=2
stdout_logfile=/dev/stdout
stdout_logfile_maxbytes=0
stderr_logfile=/dev/stderr
stderr_logfile_maxbytes=0
```

---

## STEP 7 — DOCKER COMPOSE TEMPLATES

### Template: Standard Web App (API + Nginx + Storage)
```yaml
version: '3.9'

services:

  # ── Application ──────────────────────────────────────────────────────────
  app:
    build:
      context: ../../
      dockerfile: Dockerfile
    container_name: app
    restart: unless-stopped
    environment:
      - PORT=8000                           # Override per project
      - DATABASE_URL=${DATABASE_URL}
      - API_URL=http://localhost:8000
      - ALLOWED_ORIGINS=http://localhost
      - SENTRY_DSN=${SENTRY_DSN:-}
      # Add all project-specific env vars here
    volumes:
      - app_data:/data                      # Persistent storage
      - app_logs:/app/logs
    depends_on:
      db:
        condition: service_healthy
    networks:
      - app_network
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:8000/health || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 20s

  # ── Database: Uncomment the DB your project uses ─────────────────────────

  # PostgreSQL (uncomment if project uses Postgres)
  # db:
  #   image: postgres:16-alpine
  #   environment:
  #     POSTGRES_USER: ${POSTGRES_USER:-admin}
  #     POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-changeme}
  #     POSTGRES_DB: ${POSTGRES_DB:-appdb}
  #   volumes:
  #     - postgres_data:/var/lib/postgresql/data
  #   healthcheck:
  #     test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-admin}"]
  #     interval: 10s
  #     timeout: 5s
  #     retries: 5
  #   networks:
  #     - app_network

  # MongoDB (uncomment if project uses MongoDB)
  # db:
  #   image: mongo:7
  #   environment:
  #     MONGO_INITDB_ROOT_USERNAME: ${MONGO_USER:-admin}
  #     MONGO_INITDB_ROOT_PASSWORD: ${MONGO_PASSWORD:-changeme}
  #   volumes:
  #     - mongo_data:/data/db
  #   networks:
  #     - app_network

  # Redis (uncomment if project uses Redis for caching/sessions)
  # redis:
  #   image: redis:7-alpine
  #   command: redis-server --requirepass ${REDIS_PASSWORD:-changeme}
  #   volumes:
  #     - redis_data:/data
  #   networks:
  #     - app_network

  # ── Object Storage (Self-Hosted S3 — uncomment if file uploads needed) ───
  # minio:
  #   image: minio/minio:latest
  #   command: server /data --console-address ":9001"
  #   environment:
  #     MINIO_ROOT_USER: ${MINIO_USER:-minioadmin}
  #     MINIO_ROOT_PASSWORD: ${MINIO_PASSWORD:-minioadmin123}
  #   volumes:
  #     - minio_data:/data
  #   ports:
  #     - "9000:9000"
  #     - "9001:9001"
  #   networks:
  #     - app_network

  # ── Reverse Proxy (Nginx) ─────────────────────────────────────────────────
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
  app_logs:
  # postgres_data:
  # mongo_data:
  # redis_data:
  # minio_data:

networks:
  app_network:
    driver: bridge
```

---

## STEP 8 — NGINX TEMPLATES (SELECT BY PROJECT TYPE)

### Template A: Single Backend API
```nginx
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://app:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        client_max_body_size 50M;
    }
}
```

### Template B: Streamlit / Gradio (WebSocket Required)
```nginx
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://app:8501;          # Streamlit port
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";  # WebSocket headers
        proxy_set_header Host $host;
        proxy_read_timeout 86400;
        client_max_body_size 50M;
    }

    location /api/ {
        rewrite ^/api/(.*) /$1 break;
        proxy_pass http://app:8000;          # FastAPI port
    }

    location /health {
        proxy_pass http://app:8000/health;
    }
}
```

### Template C: React/Vue SPA with Backend API
```nginx
server {
    listen 80;
    server_name _;

    root /usr/share/nginx/html;
    index index.html;

    # Serve static frontend files
    location / {
        try_files $uri $uri/ /index.html;   # SPA routing fallback
    }

    # Proxy API calls to backend
    location /api/ {
        proxy_pass http://app:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    client_max_body_size 50M;
}
```

---

## STEP 9 — PLATFORM CONFIG FILES

### render.yaml (For Render Web Service)
```yaml
services:
  - type: web
    name: your-app-name
    env: docker                            # Always Docker for full control
    dockerfilePath: ./Dockerfile
    envVars:
      - key: PORT
        value: 10000                       # Render uses 10000
      - key: NODE_ENV                      # For Node.js projects
        value: production
      - key: DATABASE_URL
        sync: false                        # Set in Render dashboard
      - key: YOUR_SECRET_KEY
        sync: false
      - key: SENTRY_DSN
        sync: false
    disk:                                  # Remove if project has no local files
      name: app-data
      mountPath: /data
      sizeGB: 1
    healthCheckPath: /health
```

### vercel.json (For Next.js / React frontends)
```json
{
  "version": 2,
  "env": {
    "NEXT_PUBLIC_API_URL": "@api_url"
  },
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "X-Frame-Options", "value": "DENY" },
        { "key": "X-XSS-Protection", "value": "1; mode=block" }
      ]
    }
  ]
}
```

---

## STEP 10 — REQUIRED APPLICATION CODE ADDITIONS

Add these to your main app file regardless of framework. Adapt syntax to
your language/framework:

### Health Check Endpoints (Required by Render, Docker, CI)

**Python (FastAPI / Flask):**
```python
import time, os
_start = time.time()

# FastAPI
@app.get("/health")
async def health():
    return {"status": "ok", "uptime": round(time.time() - _start, 2)}

@app.get("/ready")
async def ready():
    return {"status": "ready"}

@app.get("/live")
async def live():
    return {"status": "alive"}
```

**Node.js (Express):**
```javascript
const startTime = Date.now();

app.get('/health', (req, res) => {
  res.json({ status: 'ok', uptime: (Date.now() - startTime) / 1000 });
});
app.get('/ready', (req, res) => res.json({ status: 'ready' }));
app.get('/live',  (req, res) => res.json({ status: 'alive' }));
```

**Go:**
```go
http.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "application/json")
    w.Write([]byte(`{"status":"ok"}`))
})
```

### Environment-Aware Configuration (Required for any hardcoded values)

**Python:**
```python
import os
API_URL  = os.environ.get("API_URL", "http://localhost:8000")
DB_PATH  = os.environ.get("DB_PATH", "app.db")
PORT     = int(os.environ.get("PORT", 8000))
```

**Node.js:**
```javascript
const API_URL = process.env.API_URL || 'http://localhost:8000';
const PORT    = process.env.PORT    || 3000;
const DB_URL  = process.env.DATABASE_URL || 'sqlite:./app.db';
```

### CORS (Required for decoupled frontend + backend)

**Python (FastAPI):**
```python
from fastapi.middleware.cors import CORSMiddleware
origins = os.environ.get("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(CORSMiddleware, allow_origins=origins,
                   allow_methods=["*"], allow_headers=["*"])
```

**Node.js (Express):**
```javascript
const cors = require('cors');
const origins = (process.env.ALLOWED_ORIGINS || 'http://localhost:3000').split(',');
app.use(cors({ origin: origins, credentials: true }));
```

### Sentry Error Monitoring (Optional — activates only when env var is set)

**Python:**
```python
dsn = os.environ.get("SENTRY_DSN", "")
if dsn:
    import sentry_sdk
    sentry_sdk.init(dsn=dsn, traces_sample_rate=0.1)
```

**Node.js:**
```javascript
if (process.env.SENTRY_DSN) {
    const Sentry = require('@sentry/node');
    Sentry.init({ dsn: process.env.SENTRY_DSN });
}
```

---

## STEP 11 — GITHUB ACTIONS WORKFLOWS

### ci.yml — Build + Health Check
```yaml
name: CI
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
          docker run -d --name ci_app -p 8000:8000 -e PORT=8000 app:ci
          sleep 20
          curl -f http://localhost:8000/health || (docker logs ci_app && exit 1)
      - name: Cleanup
        if: always()
        run: docker rm -f ci_app
```

### lint.yml — Code Quality (auto-selects linter by language)
```yaml
name: Lint
on:
  push: {branches: [main]}
  pull_request: {branches: [main]}
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      # Python linting
      - name: Python lint (ruff)
        if: hashFiles('requirements.txt') != ''
        run: |
          pip install ruff
          ruff check . --output-format=github

      # Node.js linting
      - name: Node lint (eslint)
        if: hashFiles('package.json') != ''
        run: |
          npm ci
          npm run lint --if-present
```

### test.yml — Run Tests
```yaml
name: Test
on:
  push: {branches: [main]}
  pull_request: {branches: [main]}
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      # Python tests
      - name: Python tests
        if: hashFiles('requirements.txt') != ''
        run: |
          pip install pytest
          pip install -r requirements.txt
          [ -d "tests" ] && pytest tests/ -v || echo "No tests found, skipping"

      # Node tests
      - name: Node tests
        if: hashFiles('package.json') != ''
        run: |
          npm ci
          npm test --if-present
```

### security.yml — CVE Scan Weekly
```yaml
name: Security
on:
  push: {branches: [main]}
  schedule:
    - cron: "0 9 * * 1"
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Python CVE scan
        if: hashFiles('requirements.txt') != ''
        run: pip install pip-audit && pip-audit -r requirements.txt

      - name: Node CVE scan
        if: hashFiles('package.json') != ''
        run: npm audit --audit-level=high

      - name: Secret scan (Gitleaks)
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### release.yml — Auto GitHub Release
```yaml
name: Release
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

### deploy.yml — Trigger Render Deploy
```yaml
name: Deploy
on:
  push: {branches: [main]}
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Trigger Render deploy hook
        if: ${{ secrets.RENDER_DEPLOY_HOOK_URL != '' }}
        run: curl -X POST "${{ secrets.RENDER_DEPLOY_HOOK_URL }}"
      - run: echo "Deployment triggered successfully"
```

---

## STEP 12 — .GITIGNORE (UNIVERSAL HARDENING)

Add these to `.gitignore`:
```gitignore
# ── Secrets ───────────────────────────────────────────
.env
.env.*
!.env.example
infra/docker/.env

# ── Python ────────────────────────────────────────────
__pycache__/
*.pyc
*.pyo
venv/
.venv/
*.egg-info/
dist/
build/

# ── Node.js ───────────────────────────────────────────
node_modules/
.next/
.nuxt/
dist/
build/
*.tsbuildinfo

# ── Local databases and indexes ───────────────────────
*.db
*.sqlite
*.sqlite3
faiss_index*/
chroma_db/
*.index

# ── ML model weights (never commit large binaries) ────
*.h5
*.pkl
*.pt
*.pth
*.onnx
*.joblib
*.bin
*.safetensors
models/
weights/
checkpoints/

# ── OS and editors ────────────────────────────────────
.DS_Store
Thumbs.db
.idea/
.vscode/
*.swp

# ── Logs ──────────────────────────────────────────────
*.log
logs/
```

---

## STEP 13 — DEPLOYMENT MANUAL STEPS (BY PLATFORM)

### Render Web Service (Manual Setup — Any Project)
```
1. dashboard.render.com → New + → Web Service
2. Connect GitHub repository
3. Settings:
   - Name:     your-app-name
   - Language: Docker  ← Always Docker
   - Branch:   main
   - Region:   Oregon (US West) or closest
   - Plan:     Free
4. Environment Variables → Add each secret key
5. Advanced → Disks → Add Disk (if app stores local files):
   - Mount Path: /data
   - Size: 1 GB
6. Create Web Service
7. Live URL appears at top of dashboard after ~5 min build
```

### Vercel (Frontend — Next.js / React / Vue)
```
1. vercel.com → New Project → Import Git Repository
2. Select your repo
3. Framework: auto-detected
4. Environment Variables → Add all NEXT_PUBLIC_* and server vars
5. Deploy
6. Live URL: https://your-app.vercel.app
```

### Streamlit Community Cloud
```
1. share.streamlit.io → New App → Connect GitHub
2. Repository: your-repo
3. Branch: main
4. Main file: app/main.py (or streamlit_app/home.py)
5. Advanced → Secrets → Paste TOML format:
   API_KEY = "your_key"
   API_URL = "https://your-backend.onrender.com"
6. Deploy → Live URL: https://[app]-[hash].streamlit.app
```

### HuggingFace Spaces (Heavy ML — 16GB RAM Free)
```
1. huggingface.co → New Space
2. SDK: Docker → Blank
3. Hardware: Free (2 vCPU, 16GB RAM)
4. Visibility: Public
5. git remote add hf https://huggingface.co/spaces/[user]/[space]
   git push hf main
6. Settings → Variables and Secrets:
   PORT = 7860
   [All your API keys]
7. Live URL: https://[user]-[space].hf.space
```

---

## STEP 14 — FULL DECISION FLOWCHART

```
START: What is the frontend?
│
├── React / Vue / Svelte (pure frontend)?
│     └── Deploy to → VERCEL or CLOUDFLARE PAGES
│
├── Next.js / Remix / SvelteKit (SSR monolith)?
│     └── Deploy to → VERCEL (native)
│
├── HTML/CSS/JS (pure static)?
│     └── Deploy to → GITHUB PAGES or CLOUDFLARE PAGES
│
├── Streamlit / Gradio (Python ML UI)?
│     ├── Needs a separate backend API?
│     │     YES → Deploy both to RENDER (Docker, one container via supervisord)
│     │     NO  → Deploy to STREAMLIT COMMUNITY CLOUD
│     └── Has model weights > 500MB?
│           YES → Deploy to HUGGINGFACE SPACES (16GB RAM free)
│           NO  → RENDER (Docker)
│
└── No separate frontend (API only)?
      └── Deploy to RENDER WEB SERVICE (Docker)


BACKEND: What does it need?
│
├── WebSockets? → RENDER or HUGGINGFACE. NOT Vercel.
├── Long-running? → RENDER or HUGGINGFACE. NOT Vercel.
├── ML inference? → RENDER (< 512MB) or HUGGINGFACE (> 512MB)
└── Just REST API? → RENDER (any language via Docker)


DATABASE: What does it use?
│
├── SQLite already? → KEEP IT. Add Render persistent disk.
├── Needs real Postgres? → NEON (free, no CC)
├── Needs MongoDB? → MONGODB ATLAS (free, no CC)
├── Needs Redis? → UPSTASH REDIS (free, no CC)
└── No database? → Nothing needed.
```

---

## STEP 15 — COMMON MISTAKES (UNIVERSAL)

| ❌ Wrong | ✅ Right |
|---|---|
| Deploy Streamlit/Gradio to Vercel | Render or Streamlit Community Cloud |
| Switch SQLite to Postgres "for production" | Keep SQLite — add persistent disk |
| Commit `.env` to GitHub | Only commit `.env.example` |
| Hardcode `localhost:8000` in frontend | `process.env.API_URL \|\| "http://localhost:8000"` |
| Skip `/health` endpoint | Always add it — required by Render, Docker |
| Run Docker container as root | Use `useradd -m -u 1000 user` in Dockerfile |
| Use Google Cloud Run / AWS (credit card) | Use Render, HuggingFace, Vercel |
| Add Nginx without WebSocket headers | Add `Upgrade` + `Connection: upgrade` |
| Deploy without CI/CD | Always add 5 GitHub Actions workflows |
| Start frontend before API is ready | Use supervisord `priority` + `startsecs` |
| Migrate DB from working SQLite to Postgres | This changes app behavior — never do it |

---

*UDADP v3.0 — Universal. Tech-stack agnostic. 100% free. Zero credit cards.*
*Works for Python · Node.js · Go · React · Next.js · Vue · Streamlit · Gradio*
*and any framework, language, or architecture.*
