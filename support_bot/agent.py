"""Main agent configuration for the Support Bot."""

import os
from dotenv import load_dotenv

from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient

from support_bot.tools import (
    # Email tools
    send_email,
    read_emails,
    search_emails,
    get_unread_count,
    # WhatsApp tools
    send_whatsapp_message,
    get_whatsapp_messages,
    # LinkedIn tools
    update_linkedin_headline,
    update_linkedin_summary,
    post_linkedin_update,
    get_linkedin_profile,
)

# Load environment variables
load_dotenv()

# Agent instructions
SUPPORT_BOT_INSTRUCTIONS = """You are a helpful Support Bot that manages communication across multiple platforms.

You can help with:

📧 **Email Management:**
- Send emails to anyone
- Read recent emails from inbox
- Search for specific emails
- Check unread email count

📱 **WhatsApp Management:**
- Send WhatsApp messages to contacts
- Get information about WhatsApp Business profile
- Note: Reading messages requires webhook setup

💼 **LinkedIn Management:**
- View LinkedIn profile information
- Post updates/shares on LinkedIn
- Request headline or summary updates (may require manual steps due to API limitations)

**Guidelines:**
1. Always confirm important actions before executing (like sending messages)
2. Be clear about any limitations or manual steps needed
3. Format responses clearly with relevant details
4. Protect sensitive information
5. If credentials are not configured, explain what's needed

When asked to do something, use the appropriate tool and provide a clear summary of the result."""


def create_support_bot() -> ChatAgent:
    """Create and configure the Support Bot agent.
    
    Returns:
        A configured ChatAgent instance with all support tools
    """
    # Get GitHub token for model access
    github_token = os.getenv("GITHUB_TOKEN")
    
    if not github_token:
        raise ValueError(
            "GITHUB_TOKEN not found in environment variables. "
            "Please set it in your .env file to use GitHub Models."
        )
    
    # Create chat client using GitHub Models (free tier)
    chat_client = OpenAIChatClient(
        model_id="openai/gpt-4.1-mini",  # Using GPT-4.1-mini from GitHub Models
        api_key=github_token,
        base_url="https://models.github.ai/inference/",
    )
    
    # Create the support bot agent with all tools
    agent = ChatAgent(
        name="SupportBot",
        description="A multi-platform support bot for managing WhatsApp, Email, and LinkedIn",
        instructions=SUPPORT_BOT_INSTRUCTIONS,
        chat_client=chat_client,
        tools=[
            # Email tools
            send_email,
            read_emails,
            search_emails,
            get_unread_count,
            # WhatsApp tools
            send_whatsapp_message,
            get_whatsapp_messages,
            # LinkedIn tools
            get_linkedin_profile,
            update_linkedin_headline,
            update_linkedin_summary,
            post_linkedin_update,
        ],
    )
    
    return agent


def create_support_bot_with_openai() -> ChatAgent:
    """Create a Support Bot using OpenAI directly (requires OPENAI_API_KEY).
    
    Use this alternative if you prefer OpenAI's API directly instead of GitHub Models.
    
    Returns:
        A configured ChatAgent instance
    """
    # Create chat client using OpenAI directly
    chat_client = OpenAIChatClient(
        model_id="gpt-4o-mini",  # or "gpt-4o" for better performance
    )
    
    agent = ChatAgent(
        name="SupportBot",
        description="A multi-platform support bot for managing WhatsApp, Email, and LinkedIn",
        instructions=SUPPORT_BOT_INSTRUCTIONS,
        chat_client=chat_client,
        tools=[
            send_email,
            read_emails,
            search_emails,
            get_unread_count,
            send_whatsapp_message,
            get_whatsapp_messages,
            get_linkedin_profile,
            update_linkedin_headline,
            update_linkedin_summary,
            post_linkedin_update,
        ],
    )
    
    return agent
