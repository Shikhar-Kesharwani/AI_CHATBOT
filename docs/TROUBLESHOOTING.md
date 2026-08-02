# Troubleshooting Guide

## Hugging Face Spaces
- **OOM (Out of Memory):** If the space crashes or restarts, ensure you are not loading model weights that exceed 16GB RAM.
- **Port Binding:** Hugging Face requires the container to bind to port 7860. Check `supervisord.conf` and `Dockerfile` to ensure `PORT` is respected.

## Docker Compose
- **Database Connection Refused:** Ensure `db` container is fully healthy before the `app` starts.
- **MinIO Access Denied:** Check `S3_ACCESS_KEY_ID` and `S3_SECRET_ACCESS_KEY` in `infra/docker/.env`.
