# Deployment Guide

This project supports two primary deployment tracks:

1. **Model 1 (Cloud-Native):** Deployed to Hugging Face Spaces (Docker). See `infra/cloud/DEPLOYMENT_GUIDE.md` for step-by-step instructions.
2. **Model 2 (Self-Hosted):** Deployed using Docker Compose. Run `docker-compose -f infra/docker/docker-compose.yml up -d` on any machine with Docker installed.
