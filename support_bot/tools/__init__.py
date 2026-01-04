"""Support Bot Tools Package."""

from support_bot.tools.email_tools import (
    send_email,
    read_emails,
    search_emails,
    get_unread_count,
)
from support_bot.tools.whatsapp_tools import (
    send_whatsapp_message,
    get_whatsapp_messages,
)
from support_bot.tools.linkedin_tools import (
    update_linkedin_headline,
    update_linkedin_summary,
    post_linkedin_update,
    get_linkedin_profile,
)

__all__ = [
    # Email tools
    "send_email",
    "read_emails",
    "search_emails",
    "get_unread_count",
    # WhatsApp tools
    "send_whatsapp_message",
    "get_whatsapp_messages",
    # LinkedIn tools
    "update_linkedin_headline",
    "update_linkedin_summary",
    "post_linkedin_update",
    "get_linkedin_profile",
]
