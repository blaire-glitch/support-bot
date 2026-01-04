# Deployment Guide

## Option 1: Railway (Easiest - Free Tier)

1. Go to [railway.app](https://railway.app) and sign up with GitHub
2. Click **"New Project"** → **"Deploy from GitHub repo"**
3. Select `blaire-glitch/support-bot`
4. Add environment variables in Railway dashboard:
   - `GITHUB_TOKEN`
   - `EMAIL_ADDRESS`
   - `EMAIL_PASSWORD`
   - (Optional) WhatsApp & LinkedIn credentials
5. Railway auto-deploys! Your API will be at `https://your-app.railway.app`

## Option 2: Render (Free Tier)

1. Go to [render.com](https://render.com) and connect GitHub
2. Click **"New"** → **"Web Service"**
3. Select `blaire-glitch/support-bot`
4. Configure:
   - **Build Command:** `pip install -r requirements.txt --pre`
   - **Start Command:** `python server.py`
5. Add environment variables
6. Deploy!

## Option 3: Docker (Any Cloud/VPS)

### Local Testing
```bash
# Build and run
docker-compose up --build

# Access at http://localhost:8000
```

### Deploy to a VPS (DigitalOcean, Linode, etc.)

```bash
# SSH into your server
ssh user@your-server

# Clone repo
git clone https://github.com/blaire-glitch/support-bot.git
cd support-bot

# Create .env file with your credentials
nano .env

# Run with Docker
docker-compose up -d
```

## Option 4: Azure Container Apps

### Prerequisites
- Azure CLI installed
- Azure subscription

### Deploy

```bash
# Login to Azure
az login

# Create resource group
az group create --name support-bot-rg --location eastus

# Create Container App environment
az containerapp env create \
  --name support-bot-env \
  --resource-group support-bot-rg \
  --location eastus

# Deploy the app
az containerapp up \
  --name support-bot \
  --resource-group support-bot-rg \
  --environment support-bot-env \
  --source . \
  --env-vars \
    GITHUB_TOKEN=secretref:github-token \
    EMAIL_ADDRESS=secretref:email-address \
    EMAIL_PASSWORD=secretref:email-password
```

## API Endpoints

Once deployed, your bot exposes these endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/health` | GET | Container health check |
| `/chat` | POST | Send message to bot |
| `/email/send` | POST | Send an email |
| `/email/unread` | GET | Get unread count |
| `/email/recent` | GET | Get recent emails |

### Example API Usage

```bash
# Chat with the bot
curl -X POST https://your-app.railway.app/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "How many unread emails do I have?"}'

# Send an email
curl -X POST "https://your-app.railway.app/email/send?to=someone@example.com&subject=Hello&body=Test"
```

## Environment Variables Required

```
GITHUB_TOKEN=your_github_token
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
WHATSAPP_PHONE_NUMBER_ID=optional
WHATSAPP_ACCESS_TOKEN=optional
LINKEDIN_ACCESS_TOKEN=optional
```
