# 🌐 Cloudflare DNS + CI/CD Deployment Guide

## ✅ DNS Configuration (Cloudflare)
1. Log in to [Cloudflare Dashboard](https://dash.cloudflare.com/)
2. Go to your domain → DNS tab
3. Add the following A record:
   - **Type**: A
   - **Name**: api
   - **IPv4 address**: [your-server-ip]
   - **Proxy status**: DNS only (or Proxied for WAF)
4. SSL/TLS → Choose "Full (strict)" mode for secure API access

## 🚀 GitHub Actions for CI/CD
Automate deploy on push to main.

### 📄 .github/workflows/deploy.yml
```yaml
name: Deploy Banking API

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: SSH Deploy
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.SERVER_IP }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SSH_KEY }}
          script: |
            cd /home/ubuntu/banking-api-complete
            git pull origin main
            docker-compose down
            docker-compose up --build -d
```

### 🔐 GitHub Secrets Required
- `SERVER_IP`
- `SERVER_USER`
- `SSH_KEY` (private key of deploy user)

## 📦 Directory structure
- `README.md`: This file
- `.github/workflows/deploy.yml`: Sample GitHub Action
