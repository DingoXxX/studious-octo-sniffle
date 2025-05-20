#!/bin/bash
# Install NGINX and Certbot
sudo apt update
sudo apt install nginx certbot python3-certbot-nginx -y

# Reload NGINX to apply config
sudo systemctl reload nginx

# Replace api.yourdomain.com with your actual domain
sudo certbot --nginx -d api.yourdomain.com

# Test auto-renewal
sudo certbot renew --dry-run
