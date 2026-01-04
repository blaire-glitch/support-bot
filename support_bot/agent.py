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
    # Desktop automation tools
    open_application,
    close_application,
    list_running_apps,
    take_screenshot,
    create_folder,
    list_files,
    open_file,
    move_file,
    delete_file,
    create_text_file,
    # File organization tools
    organize_files,
    preview_organization,
    organize_by_date,
    cleanup_empty_folders,
    find_duplicates,
    find_large_files,
    get_folder_stats,
    # System tools
    get_system_info,
    get_battery_status,
    run_command,
    get_resource_usage,
    kill_process,
    open_website,
    search_google,
    copy_to_clipboard,
    get_clipboard,
    set_volume,
    mute_volume,
    lock_screen,
    empty_recycle_bin,
    # Notes & Reminders
    create_note,
    list_notes,
    delete_note,
    show_notification,
    set_timer,
    # Network
    get_network_info,
    test_internet_connection,
    # Weather
    get_weather,
    # Workflows
    morning_routine,
    end_of_day,
    quick_cleanup,
    # Display
    set_brightness,
    get_brightness,
    # Text
    text_to_speech,
    type_text,
    # Startup
    list_startup_apps,
    # Windows
    minimize_all_windows,
    restore_all_windows,
)

# Load environment variables
load_dotenv()

# Agent instructions
SUPPORT_BOT_INSTRUCTIONS = """You are a helpful Support Bot that manages communication and automates desktop tasks.

You can help with:

📧 **Email Management:**
- Send emails, read inbox, search emails, check unread count

📱 **WhatsApp Management:**
- Send WhatsApp messages, get profile info

💼 **LinkedIn Management:**
- View profile, post updates, update headline/summary

🖥️ **Desktop Automation:**
- Open/close applications (Chrome, Word, Excel, Notepad, VS Code, etc.)
- Take screenshots, browse files, create/move/delete files
- Run shell commands, open websites, search Google
- Copy/paste clipboard, control volume, lock screen

📂 **File Organization:**
- Organize files by type or date in Desktop/Downloads/Documents
- Find duplicates, find large files, get folder statistics
- Preview before moving, clean up empty folders

📝 **Notes & Reminders:**
- Create, list, and delete quick notes
- Set timers with notifications
- Show desktop notifications

🌐 **Network & Connectivity:**
- Get network/WiFi info, test internet connection
- Show IP address and signal strength

☀️ **Weather:**
- Get current weather for any city

📊 **System Monitoring:**
- CPU, RAM, disk usage
- Kill unresponsive processes
- List top memory consumers
- List startup applications

🪟 **Window Management:**
- Minimize all windows (show desktop)
- Restore all windows

☀️ **Display:**
- Adjust screen brightness

🔊 **Text-to-Speech:**
- Read text aloud
- Auto-type text

⚡ **Quick Workflows:**
- Morning routine (open work apps)
- End of day summary
- Quick cleanup (empty recycle bin, clear temp files)

**Guidelines:**
1. Always confirm important/destructive actions before executing
2. For file organization, offer to preview first before actually moving files
3. Be clear about any limitations
4. Format responses clearly with relevant details
5. Protect sensitive information
6. For file deletion, require explicit confirmation

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
        description="A multi-platform support bot for managing WhatsApp, Email, LinkedIn and desktop automation",
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
            # Desktop automation tools
            open_application,
            close_application,
            list_running_apps,
            take_screenshot,
            create_folder,
            list_files,
            open_file,
            move_file,
            delete_file,
            create_text_file,
            # File organization tools
            organize_files,
            preview_organization,
            organize_by_date,
            cleanup_empty_folders,
            find_duplicates,
            find_large_files,
            get_folder_stats,
            # System tools
            get_system_info,
            get_battery_status,
            run_command,
            get_resource_usage,
            kill_process,
            open_website,
            search_google,
            copy_to_clipboard,
            get_clipboard,
            set_volume,
            mute_volume,
            lock_screen,
            empty_recycle_bin,
            # Notes & Reminders
            create_note,
            list_notes,
            delete_note,
            show_notification,
            set_timer,
            # Network
            get_network_info,
            test_internet_connection,
            # Weather
            get_weather,
            # Workflows
            morning_routine,
            end_of_day,
            quick_cleanup,
            # Display
            set_brightness,
            get_brightness,
            # Text
            text_to_speech,
            type_text,
            # Startup
            list_startup_apps,
            # Windows
            minimize_all_windows,
            restore_all_windows,
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
