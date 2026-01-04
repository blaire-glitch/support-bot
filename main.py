#!/usr/bin/env python3
"""
Support Bot - Main Entry Point

An AI-powered support bot to manage WhatsApp, Email, and LinkedIn.
Uses Microsoft Agent Framework with GitHub Models (free tier).
"""

import asyncio
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def print_banner():
    """Print the welcome banner."""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   🤖 SUPPORT BOT - Multi-Platform Communication Manager          ║
║                                                                  ║
║   📧 Email    │  📱 WhatsApp    │  💼 LinkedIn                   ║
║                                                                  ║
║   Type 'help' for available commands, 'quit' to exit            ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
    """)


def print_help():
    """Print help information."""
    print("""
📋 **Available Commands:**

**Email:**
  • "Send an email to [email] about [subject]"
  • "Read my recent emails"
  • "Search emails for [query]"
  • "How many unread emails do I have?"

**WhatsApp:**
  • "Send a WhatsApp message to [phone] saying [message]"
  • "Get my WhatsApp business profile"

**LinkedIn:**
  • "Show my LinkedIn profile"
  • "Post on LinkedIn: [your update]"
  • "Update my LinkedIn headline to [new headline]"

**System:**
  • help  - Show this help message
  • quit  - Exit the bot
  • clear - Clear the screen

💡 **Tip:** Just describe what you want in natural language!
    """)


def check_configuration():
    """Check and report on configuration status."""
    print("\n📋 **Configuration Status:**\n")
    
    # GitHub Token (required)
    github_token = os.getenv("GITHUB_TOKEN")
    if github_token:
        print("  ✅ GitHub Token: Configured")
    else:
        print("  ❌ GitHub Token: NOT SET (Required!)")
        print("     Get a token at: https://github.com/settings/tokens")
    
    # Email
    email_configured = os.getenv("EMAIL_ADDRESS") and os.getenv("EMAIL_PASSWORD")
    if email_configured:
        print(f"  ✅ Email: Configured ({os.getenv('EMAIL_ADDRESS')})")
    else:
        print("  ⚠️  Email: Not configured")
    
    # WhatsApp
    whatsapp_configured = os.getenv("WHATSAPP_PHONE_NUMBER_ID") and os.getenv("WHATSAPP_ACCESS_TOKEN")
    if whatsapp_configured:
        print("  ✅ WhatsApp: Configured")
    else:
        print("  ⚠️  WhatsApp: Not configured")
    
    # LinkedIn
    linkedin_configured = os.getenv("LINKEDIN_ACCESS_TOKEN")
    if linkedin_configured:
        print("  ✅ LinkedIn: Configured")
    else:
        print("  ⚠️  LinkedIn: Not configured")
    
    print()
    
    return github_token is not None


async def interactive_chat():
    """Run the interactive chat loop."""
    from support_bot import create_support_bot
    
    print_banner()
    
    # Check configuration
    if not check_configuration():
        print("❌ Cannot start: GITHUB_TOKEN is required.")
        print("   Create a .env file with your GitHub Personal Access Token.")
        print("   See .env.example for the template.\n")
        return
    
    print("🚀 Starting Support Bot...\n")
    
    try:
        bot = create_support_bot()
        print("✅ Support Bot is ready! How can I help you today?\n")
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
        return
    
    # Chat history for context
    conversation_history = []
    
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            # Handle special commands
            if user_input.lower() == "quit":
                print("\n👋 Goodbye! Thanks for using Support Bot.\n")
                break
            elif user_input.lower() == "help":
                print_help()
                continue
            elif user_input.lower() == "clear":
                os.system("cls" if os.name == "nt" else "clear")
                print_banner()
                continue
            elif user_input.lower() == "status":
                check_configuration()
                continue
            
            # Send to bot
            print("\n🤔 Thinking...\n")
            
            try:
                result = await bot.run(user_input)
                print(f"Bot: {result.text}\n")
            except Exception as e:
                print(f"❌ Error: {e}\n")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!\n")
            break


async def run_single_command(command: str):
    """Run a single command and exit."""
    from support_bot import create_support_bot
    
    # Check for GitHub token
    if not os.getenv("GITHUB_TOKEN"):
        print("Error: GITHUB_TOKEN not configured.")
        return
    
    bot = create_support_bot()
    result = await bot.run(command)
    print(result.text)


def main():
    """Main entry point."""
    # Check if running with a command argument
    if len(sys.argv) > 1:
        command = " ".join(sys.argv[1:])
        asyncio.run(run_single_command(command))
    else:
        # Interactive mode
        asyncio.run(interactive_chat())


if __name__ == "__main__":
    main()
