FROM python:3.10-slim

# ─────────────────────────────────────────────────────────────────────────────
# SYSTEM DEPENDENCIES
# Supervisord is used to run FastAPI + Streamlit in one container
# ─────────────────────────────────────────────────────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# ─────────────────────────────────────────────────────────────────────────────
# NON-ROOT USER
# Required by Hugging Face Spaces and good practice for all platforms
# ─────────────────────────────────────────────────────────────────────────────
RUN useradd -m -u 1000 user
USER user

ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

# ─────────────────────────────────────────────────────────────────────────────
# DEPENDENCIES (installed before copying source for Docker layer caching)
# ─────────────────────────────────────────────────────────────────────────────
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ─────────────────────────────────────────────────────────────────────────────
# APPLICATION CODE
# ─────────────────────────────────────────────────────────────────────────────
COPY --chown=user . .

# ─────────────────────────────────────────────────────────────────────────────
# PORTS
# 8000 = FastAPI backend (internal)
# 7860 = Streamlit frontend (public — required by Hugging Face Spaces)
# 8501 = Streamlit alternate (for Render / Docker Compose)
# PORT env var is read by supervisord.conf for flexibility
# ─────────────────────────────────────────────────────────────────────────────
EXPOSE 8000 7860 8501

# ─────────────────────────────────────────────────────────────────────────────
# STARTUP
# Supervisord launches both FastAPI and Streamlit simultaneously
# ─────────────────────────────────────────────────────────────────────────────
CMD ["supervisord", "-c", "supervisord.conf"]
