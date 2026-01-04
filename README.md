# Support Bot - WhatsApp, Email & LinkedIn Manager

A multi-service AI agent bot built with Microsoft Agent Framework to help manage your WhatsApp messages, emails, and LinkedIn profile.

## Features

- 📱 **WhatsApp Management** - Send messages, read conversations
- 📧 **Email Management** - Send emails, read inbox, search emails
- 💼 **LinkedIn Management** - Update profile, post updates, manage connections

## Prerequisites

1. **Python 3.10+**
2. **GitHub Personal Access Token (PAT)** - For free AI model access
3. **Service API credentials** (see Configuration section)

## Installation

```bash
# Navigate to project directory
cd support-bot

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
# source .venv/bin/activate

# Install dependencies (--pre flag is required for Agent Framework preview)
pip install -r requirements.txt --pre
```

## Configuration

Create a `.env` file in the project root with your credentials:

```env
# GitHub Models (Free tier)
GITHUB_TOKEN=your_github_personal_access_token

# Email Configuration (Gmail example)
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
IMAP_SERVER=imap.gmail.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# WhatsApp Business API (Optional - requires Meta Business account)
WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id
WHATSAPP_ACCESS_TOKEN=your_access_token

# LinkedIn API (Optional - requires LinkedIn Developer App)
LINKEDIN_CLIENT_ID=your_client_id
LINKEDIN_CLIENT_SECRET=your_client_secret
LINKEDIN_ACCESS_TOKEN=your_access_token
```

### Getting API Credentials

#### GitHub PAT (Required)
1. Go to https://github.com/settings/tokens
2. Generate a new token (classic) with no specific scopes needed
3. Copy the token to `GITHUB_TOKEN`

#### Gmail App Password
1. Enable 2-factor authentication on your Google account
2. Go to https://myaccount.google.com/apppasswords
3. Generate an app password for "Mail"
4. Use this as `EMAIL_PASSWORD`

#### WhatsApp Business API (Optional)
1. Create a Meta Business account at https://business.facebook.com
2. Set up WhatsApp Business API
3. Get your Phone Number ID and Access Token from the dashboard

#### LinkedIn API (Optional)
1. Go to https://www.linkedin.com/developers/apps
2. Create a new app
3. Request access to the required API products
4. Get your Client ID, Client Secret, and generate an Access Token

## Usage

### Interactive Chat Mode

```bash
python main.py
```

Then interact with the bot using natural language:

```
You: Send an email to john@example.com saying "Meeting at 3pm tomorrow"
Bot: I've sent the email to john@example.com with the subject "Meeting Reminder"...

You: What unread emails do I have?
Bot: You have 3 unread emails...

You: Send a WhatsApp message to +1234567890 saying "Hello!"
Bot: Message sent successfully to +1234567890...

You: Update my LinkedIn headline to "Senior Software Engineer | AI Enthusiast"
Bot: Your LinkedIn headline has been updated...
```

### Programmatic Usage

```python
import asyncio
from support_bot import create_support_bot

async def main():
    bot = create_support_bot()
    
    # Send an email
    result = await bot.run("Send an email to boss@company.com about the project update")
    print(result.text)
    
    # Check WhatsApp
    result = await bot.run("Read my recent WhatsApp messages")
    print(result.text)

asyncio.run(main())
```

## Project Structure

```
support-bot/
├── README.md
├── requirements.txt
├── .env.example
├── main.py                 # Main entry point
├── support_bot/
│   ├── __init__.py
│   ├── agent.py           # Main agent configuration
│   └── tools/
│       ├── __init__.py
│       ├── email_tools.py     # Email send/read tools
│       ├── whatsapp_tools.py  # WhatsApp messaging tools
│       └── linkedin_tools.py  # LinkedIn profile tools
└── tests/
    └── test_tools.py
```

## Troubleshooting

### Common Issues

1. **"Rate limit exceeded"** - You've hit the GitHub Models free tier limit. Wait or upgrade.
2. **"SMTP Authentication failed"** - Check your email app password configuration.
3. **"WhatsApp API error"** - Verify your WhatsApp Business API credentials.

## License

MIT License
