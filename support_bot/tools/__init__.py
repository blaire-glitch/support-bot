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
from support_bot.tools.desktop_tools import (
    # Application control
    open_application,
    close_application,
    list_running_apps,
    # Screenshot
    take_screenshot,
    # File operations
    create_folder,
    list_files,
    open_file,
    move_file,
    delete_file,
    create_text_file,
    # File organization
    organize_files,
    preview_organization,
    organize_by_date,
    cleanup_empty_folders,
    find_duplicates,
    find_large_files,
    get_folder_stats,
    # System
    get_system_info,
    get_battery_status,
    run_command,
    get_resource_usage,
    kill_process,
    # Web
    open_website,
    search_google,
    # Clipboard
    copy_to_clipboard,
    get_clipboard,
    # Volume
    set_volume,
    mute_volume,
    # Quick actions
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
    # Desktop tools - Application control
    "open_application",
    "close_application",
    "list_running_apps",
    # Desktop tools - Screenshot
    "take_screenshot",
    # Desktop tools - File operations
    "create_folder",
    "list_files",
    "open_file",
    "move_file",
    "delete_file",
    "create_text_file",
    # Desktop tools - File organization
    "organize_files",
    "preview_organization",
    "organize_by_date",
    "cleanup_empty_folders",
    "find_duplicates",
    "find_large_files",
    "get_folder_stats",
    # Desktop tools - System
    "get_system_info",
    "get_battery_status",
    "run_command",
    "get_resource_usage",
    "kill_process",
    # Desktop tools - Web
    "open_website",
    "search_google",
    # Desktop tools - Clipboard
    "copy_to_clipboard",
    "get_clipboard",
    # Desktop tools - Volume
    "set_volume",
    "mute_volume",
    # Desktop tools - Quick actions
    "lock_screen",
    "empty_recycle_bin",
    # Notes & Reminders
    "create_note",
    "list_notes",
    "delete_note",
    "show_notification",
    "set_timer",
    # Network
    "get_network_info",
    "test_internet_connection",
    # Weather
    "get_weather",
    # Workflows
    "morning_routine",
    "end_of_day",
    "quick_cleanup",
    # Display
    "set_brightness",
    "get_brightness",
    # Text
    "text_to_speech",
    "type_text",
    # Startup
    "list_startup_apps",
    # Windows
    "minimize_all_windows",
    "restore_all_windows",
]
