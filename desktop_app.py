"""
Support Bot Desktop Application with Avatar
A floating desktop assistant you can chat with anytime.
"""

import os
import sys
import threading
import asyncio
import json
import tkinter as tk
from tkinter import ttk, scrolledtext
import webbrowser
from pathlib import Path

# Add the project to path
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / ".env")


class AvatarWindow:
    """Floating avatar that expands into chat."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Support Bot")
        self.root.overrideredirect(True)  # Remove window decorations
        self.root.attributes('-topmost', True)  # Always on top
        self.root.attributes('-alpha', 0.95)  # Slight transparency
        
        # Window state
        self.expanded = False
        self.drag_data = {"x": 0, "y": 0}
        self.is_dragging = False
        
        # Colors
        self.bg_color = "#1a1a2e"
        self.accent_color = "#3b82f6"
        self.text_color = "#ffffff"
        self.input_bg = "#16213e"
        
        # Initialize bot
        self.bot = None
        self.bot_ready = False
        self.init_bot_async()
        
        # Create UI
        self.create_avatar()
        
        # Position in bottom-right corner
        self.position_window()
        
    def init_bot_async(self):
        """Initialize bot in background thread."""
        def init():
            try:
                from support_bot import create_support_bot
                self.bot = create_support_bot()
                self.bot_ready = True
                self.root.after(0, lambda: self.status_label.config(text="● Online", fg="#4ade80"))
            except Exception as e:
                print(f"Bot init error: {e}")
                self.root.after(0, lambda: self.status_label.config(text="● Offline", fg="#f87171"))
        
        thread = threading.Thread(target=init, daemon=True)
        thread.start()
        
    def create_avatar(self):
        """Create the avatar button and chat interface."""
        # Main container
        self.main_frame = tk.Frame(self.root, bg=self.bg_color)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Avatar button (always visible)
        self.avatar_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.avatar_frame.pack(fill=tk.X)
        
        # Avatar circle with robot emoji
        self.avatar_btn = tk.Label(
            self.avatar_frame,
            text="🤖",
            font=("Segoe UI Emoji", 32),
            bg=self.accent_color,
            fg=self.text_color,
            width=3,
            height=1,
            cursor="hand2"
        )
        self.avatar_btn.pack(side=tk.LEFT, padx=5, pady=5)
        self.avatar_btn.bind("<ButtonPress-1>", self.start_drag)
        self.avatar_btn.bind("<B1-Motion>", self.drag_window)
        self.avatar_btn.bind("<ButtonRelease-1>", self.on_click_release)
        
        # Status and title (collapsed view)
        self.header_info = tk.Frame(self.avatar_frame, bg=self.bg_color)
        self.header_info.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        self.title_label = tk.Label(
            self.header_info,
            text="Support Bot",
            font=("Segoe UI", 11, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        self.title_label.pack(anchor=tk.W)
        
        self.status_label = tk.Label(
            self.header_info,
            text="● Starting...",
            font=("Segoe UI", 9),
            bg=self.bg_color,
            fg="#fbbf24"
        )
        self.status_label.pack(anchor=tk.W)
        
        # Close button
        self.close_btn = tk.Label(
            self.avatar_frame,
            text="✕",
            font=("Segoe UI", 12),
            bg=self.bg_color,
            fg="#888",
            cursor="hand2",
            padx=10
        )
        self.close_btn.pack(side=tk.RIGHT)
        self.close_btn.bind("<Button-1>", lambda e: self.root.quit())
        self.close_btn.bind("<Enter>", lambda e: self.close_btn.config(fg="#f87171"))
        self.close_btn.bind("<Leave>", lambda e: self.close_btn.config(fg="#888"))
        
        # Chat container (hidden initially)
        self.chat_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        
        # Chat display
        self.chat_display = scrolledtext.ScrolledText(
            self.chat_frame,
            wrap=tk.WORD,
            font=("Segoe UI", 10),
            bg=self.input_bg,
            fg=self.text_color,
            insertbackground=self.text_color,
            relief=tk.FLAT,
            height=15,
            width=40,
            state=tk.DISABLED
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 5))
        
        # Configure tags for styling
        self.chat_display.tag_configure("user", foreground="#60a5fa", font=("Segoe UI", 10, "bold"))
        self.chat_display.tag_configure("bot", foreground="#4ade80", font=("Segoe UI", 10, "bold"))
        self.chat_display.tag_configure("message", foreground=self.text_color)
        
        # Quick action buttons - Row 1 (Email)
        self.quick_frame1 = tk.Frame(self.chat_frame, bg=self.bg_color)
        self.quick_frame1.pack(fill=tk.X, padx=10, pady=(5, 2))
        
        quick_actions_email = [
            ("📧 Emails", "How many unread emails?"),
            ("📬 Read", "Read latest 3 emails"),
        ]
        
        for text, cmd in quick_actions_email:
            btn = tk.Button(
                self.quick_frame1,
                text=text,
                font=("Segoe UI", 9),
                bg=self.input_bg,
                fg=self.text_color,
                activebackground=self.accent_color,
                activeforeground=self.text_color,
                relief=tk.FLAT,
                cursor="hand2",
                command=lambda c=cmd: self.send_quick(c)
            )
            btn.pack(side=tk.LEFT, padx=2)
        
        # Quick action buttons - Row 2 (Desktop)
        self.quick_frame2 = tk.Frame(self.chat_frame, bg=self.bg_color)
        self.quick_frame2.pack(fill=tk.X, padx=10, pady=(0, 2))
        
        quick_actions_desktop = [
            ("📸 Screenshot", "Take a screenshot"),
            ("💻 System", "Get system info"),
            ("🔋 Battery", "Check battery status"),
        ]
        
        for text, cmd in quick_actions_desktop:
            btn = tk.Button(
                self.quick_frame2,
                text=text,
                font=("Segoe UI", 9),
                bg=self.input_bg,
                fg=self.text_color,
                activebackground=self.accent_color,
                activeforeground=self.text_color,
                relief=tk.FLAT,
                cursor="hand2",
                command=lambda c=cmd: self.send_quick(c)
            )
            btn.pack(side=tk.LEFT, padx=2)
        
        # Quick action buttons - Row 3 (File Organization)
        self.quick_frame3 = tk.Frame(self.chat_frame, bg=self.bg_color)
        self.quick_frame3.pack(fill=tk.X, padx=10, pady=(0, 5))
        
        quick_actions_files = [
            ("📂 Organize", "Preview organizing my Downloads folder"),
            ("📊 Stats", "Get folder stats for Downloads"),
        ]
        
        for text, cmd in quick_actions_files:
            btn = tk.Button(
                self.quick_frame3,
                text=text,
                font=("Segoe UI", 9),
                bg=self.input_bg,
                fg=self.text_color,
                activebackground=self.accent_color,
                activeforeground=self.text_color,
                relief=tk.FLAT,
                cursor="hand2",
                command=lambda c=cmd: self.send_quick(c)
            )
            btn.pack(side=tk.LEFT, padx=2)
        
        # Input area
        self.input_frame = tk.Frame(self.chat_frame, bg=self.bg_color)
        self.input_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.input_entry = tk.Entry(
            self.input_frame,
            font=("Segoe UI", 11),
            bg=self.input_bg,
            fg=self.text_color,
            insertbackground=self.text_color,
            relief=tk.FLAT
        )
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, padx=(0, 5))
        self.input_entry.bind("<Return>", self.send_message)
        
        self.send_btn = tk.Button(
            self.input_frame,
            text="➤",
            font=("Segoe UI", 14),
            bg=self.accent_color,
            fg=self.text_color,
            activebackground="#2563eb",
            activeforeground=self.text_color,
            relief=tk.FLAT,
            cursor="hand2",
            command=self.send_message,
            width=3
        )
        self.send_btn.pack(side=tk.RIGHT)
        
        # Add welcome message
        self.add_message("Bot", "👋 Hi! I can help with emails, WhatsApp, LinkedIn, and automate your desktop! Try: 'open chrome', 'take screenshot', 'what apps are running?'")
        
    def position_window(self):
        """Position window in bottom-right corner."""
        self.root.update_idletasks()
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        
        # Start with collapsed size
        self.root.geometry(f"280x70+{screen_w - 300}+{screen_h - 150}")
        
    def start_drag(self, event):
        """Start dragging the window."""
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        self.is_dragging = False
        
    def drag_window(self, event):
        """Drag the window."""
        # Check if we've moved enough to consider it a drag
        dx = abs(event.x - self.drag_data["x"])
        dy = abs(event.y - self.drag_data["y"])
        if dx > 5 or dy > 5:
            self.is_dragging = True
        
        x = self.root.winfo_x() + (event.x - self.drag_data["x"])
        y = self.root.winfo_y() + (event.y - self.drag_data["y"])
        self.root.geometry(f"+{x}+{y}")
        
    def on_click_release(self, event):
        """Handle click release - toggle chat only if not dragging."""
        if not self.is_dragging:
            self.toggle_chat()
        
    def toggle_chat(self, event=None):
        """Toggle between avatar and full chat view."""
        if self.expanded:
            # Collapse
            self.chat_frame.pack_forget()
            self.root.geometry(f"280x70")
            self.expanded = False
        else:
            # Expand
            self.chat_frame.pack(fill=tk.BOTH, expand=True)
            self.root.geometry(f"380x450")
            self.input_entry.focus_set()
            self.expanded = True
            
    def add_message(self, sender, message):
        """Add a message to the chat display."""
        self.chat_display.config(state=tk.NORMAL)
        
        if sender == "You":
            self.chat_display.insert(tk.END, f"\n{sender}: ", "user")
        else:
            self.chat_display.insert(tk.END, f"\n{sender}: ", "bot")
            
        self.chat_display.insert(tk.END, f"{message}\n", "message")
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
        
    def send_quick(self, message):
        """Send a quick action message."""
        if not self.expanded:
            self.toggle_chat()
        self.input_entry.delete(0, tk.END)
        self.input_entry.insert(0, message)
        self.send_message()
        
    def send_message(self, event=None):
        """Send a message to the bot."""
        message = self.input_entry.get().strip()
        if not message:
            return
            
        self.input_entry.delete(0, tk.END)
        self.add_message("You", message)
        
        if not self.bot_ready:
            self.add_message("Bot", "⏳ Still starting up, please wait...")
            return
            
        # Disable input while processing
        self.input_entry.config(state=tk.DISABLED)
        self.send_btn.config(state=tk.DISABLED)
        self.add_message("Bot", "💭 Thinking...")
        
        # Process in background
        def process():
            try:
                # Run the async bot.run() method properly
                result = asyncio.run(self.bot.run(message))
                response = result.text  # Extract the text from AgentRunResponse
                # Remove "Thinking..." and add real response
                self.root.after(0, lambda: self.update_last_message(response))
            except Exception as e:
                self.root.after(0, lambda: self.update_last_message(f"❌ Error: {str(e)}"))
            finally:
                self.root.after(0, self.enable_input)
                
        thread = threading.Thread(target=process, daemon=True)
        thread.start()
        
    def update_last_message(self, new_text):
        """Update the last bot message."""
        self.chat_display.config(state=tk.NORMAL)
        # Find and delete the "Thinking..." message
        content = self.chat_display.get("1.0", tk.END)
        thinking_pos = content.rfind("💭 Thinking...")
        if thinking_pos != -1:
            # Delete from "Bot: 💭 Thinking..." to end
            self.chat_display.delete("end-3l", "end-1c")
            self.chat_display.insert(tk.END, f"{new_text}\n", "message")
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
        
    def enable_input(self):
        """Re-enable input after processing."""
        self.input_entry.config(state=tk.NORMAL)
        self.send_btn.config(state=tk.NORMAL)
        self.input_entry.focus_set()
        
    def run(self):
        """Start the application."""
        self.root.mainloop()


def main():
    """Entry point for desktop app."""
    app = AvatarWindow()
    app.run()


if __name__ == "__main__":
    main()
