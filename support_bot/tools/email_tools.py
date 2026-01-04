"""Email management tools for the support bot."""

import os
import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import decode_header
from typing import Annotated
from datetime import datetime
from pydantic import Field


def send_email(
    to: Annotated[str, Field(description="Recipient email address")],
    subject: Annotated[str, Field(description="Email subject line")],
    body: Annotated[str, Field(description="Email body content")],
    cc: Annotated[str | None, Field(description="CC recipients (comma-separated)")] = None,
) -> str:
    """Send an email to the specified recipient.
    
    Args:
        to: The recipient's email address
        subject: The subject line of the email
        body: The main content of the email
        cc: Optional CC recipients (comma-separated)
        
    Returns:
        A confirmation message with the result
    """
    email_address = os.getenv("EMAIL_ADDRESS")
    email_password = os.getenv("EMAIL_PASSWORD")
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    
    if not email_address or not email_password:
        return "Error: Email credentials not configured. Please set EMAIL_ADDRESS and EMAIL_PASSWORD in .env file."
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg["From"] = email_address
        msg["To"] = to
        msg["Subject"] = subject
        
        if cc:
            msg["Cc"] = cc
        
        msg.attach(MIMEText(body, "plain"))
        
        # Send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(email_address, email_password)
            
            recipients = [to]
            if cc:
                recipients.extend([addr.strip() for addr in cc.split(",")])
            
            server.sendmail(email_address, recipients, msg.as_string())
        
        return f"✅ Email sent successfully to {to}" + (f" (CC: {cc})" if cc else "")
        
    except smtplib.SMTPAuthenticationError:
        return "Error: Email authentication failed. Check your EMAIL_PASSWORD (use an app password for Gmail)."
    except Exception as e:
        return f"Error sending email: {str(e)}"


def read_emails(
    count: Annotated[int, Field(description="Number of recent emails to read")] = 5,
    folder: Annotated[str, Field(description="Email folder: INBOX, SPAM, TRASH, SENT, DRAFTS, or STARRED")] = "INBOX",
) -> str:
    """Read recent emails from the specified folder.
    
    Args:
        count: Number of emails to retrieve (default: 5)
        folder: The folder to read from. Options: INBOX, SPAM, TRASH, SENT, DRAFTS, STARRED
        
    Returns:
        A formatted list of recent emails
    """
    email_address = os.getenv("EMAIL_ADDRESS")
    email_password = os.getenv("EMAIL_PASSWORD")
    imap_server = os.getenv("IMAP_SERVER", "imap.gmail.com")
    
    if not email_address or not email_password:
        return "Error: Email credentials not configured. Please set EMAIL_ADDRESS and EMAIL_PASSWORD in .env file."
    
    # Map common folder names to Gmail folder names
    folder_map = {
        "SPAM": "[Gmail]/Spam",
        "TRASH": "[Gmail]/Trash", 
        "SENT": "[Gmail]/Sent Mail",
        "DRAFTS": "[Gmail]/Drafts",
        "STARRED": "[Gmail]/Starred",
        "ALL": "[Gmail]/All Mail",
        "IMPORTANT": "[Gmail]/Important",
    }
    gmail_folder = folder_map.get(folder.upper(), folder)
    
    try:
        # Connect to IMAP server
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(email_address, email_password)
        mail.select(gmail_folder)
        
        # Search for all emails
        _, message_numbers = mail.search(None, "ALL")
        email_ids = message_numbers[0].split()
        
        if not email_ids:
            mail.logout()
            return f"No emails found in {folder}."
        
        # Get the last 'count' emails
        recent_ids = email_ids[-count:]
        emails = []
        
        for email_id in reversed(recent_ids):
            _, msg_data = mail.fetch(email_id, "(RFC822)")
            email_body = msg_data[0][1]
            msg = email.message_from_bytes(email_body)
            
            # Decode subject
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or "utf-8")
            
            # Get sender
            sender = msg["From"]
            
            # Get date
            date = msg["Date"]
            
            # Get a preview of the body
            body_preview = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body_preview = part.get_payload(decode=True).decode("utf-8", errors="ignore")[:100]
                        break
            else:
                body_preview = msg.get_payload(decode=True).decode("utf-8", errors="ignore")[:100]
            
            emails.append({
                "from": sender,
                "subject": subject,
                "date": date,
                "preview": body_preview.replace("\n", " ").strip()
            })
        
        mail.logout()
        
        # Format output
        result = f"📧 Recent {len(emails)} emails from {folder}:\n\n"
        for i, e in enumerate(emails, 1):
            result += f"{i}. **From:** {e['from']}\n"
            result += f"   **Subject:** {e['subject']}\n"
            result += f"   **Date:** {e['date']}\n"
            result += f"   **Preview:** {e['preview']}...\n\n"
        
        return result
        
    except imaplib.IMAP4.error as e:
        return f"Error accessing email: {str(e)}"
    except Exception as e:
        return f"Error reading emails: {str(e)}"


def search_emails(
    query: Annotated[str, Field(description="Search query (searches in subject and sender)")],
    count: Annotated[int, Field(description="Maximum number of results")] = 10,
) -> str:
    """Search emails by subject or sender.
    
    Args:
        query: The search term to look for
        count: Maximum number of results to return
        
    Returns:
        A list of matching emails
    """
    email_address = os.getenv("EMAIL_ADDRESS")
    email_password = os.getenv("EMAIL_PASSWORD")
    imap_server = os.getenv("IMAP_SERVER", "imap.gmail.com")
    
    if not email_address or not email_password:
        return "Error: Email credentials not configured."
    
    try:
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(email_address, email_password)
        mail.select("INBOX")
        
        # Search in subject
        _, subject_results = mail.search(None, f'SUBJECT "{query}"')
        # Search in from
        _, from_results = mail.search(None, f'FROM "{query}"')
        
        # Combine results
        all_ids = set(subject_results[0].split() + from_results[0].split())
        
        if not all_ids:
            mail.logout()
            return f"No emails found matching '{query}'."
        
        # Get the most recent matches
        sorted_ids = sorted(all_ids, reverse=True)[:count]
        emails = []
        
        for email_id in sorted_ids:
            _, msg_data = mail.fetch(email_id, "(RFC822)")
            email_body = msg_data[0][1]
            msg = email.message_from_bytes(email_body)
            
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or "utf-8")
            
            emails.append({
                "from": msg["From"],
                "subject": subject,
                "date": msg["Date"]
            })
        
        mail.logout()
        
        result = f"🔍 Found {len(emails)} emails matching '{query}':\n\n"
        for i, e in enumerate(emails, 1):
            result += f"{i}. **From:** {e['from']}\n"
            result += f"   **Subject:** {e['subject']}\n"
            result += f"   **Date:** {e['date']}\n\n"
        
        return result
        
    except Exception as e:
        return f"Error searching emails: {str(e)}"


def get_unread_count() -> str:
    """Get the count of unread emails in the inbox.
    
    Returns:
        The number of unread emails
    """
    email_address = os.getenv("EMAIL_ADDRESS")
    email_password = os.getenv("EMAIL_PASSWORD")
    imap_server = os.getenv("IMAP_SERVER", "imap.gmail.com")
    
    if not email_address or not email_password:
        return "Error: Email credentials not configured."
    
    try:
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(email_address, email_password)
        mail.select("INBOX")
        
        _, messages = mail.search(None, "UNSEEN")
        unread_count = len(messages[0].split()) if messages[0] else 0
        
        mail.logout()
        
        if unread_count == 0:
            return "📬 You have no unread emails."
        elif unread_count == 1:
            return "📫 You have 1 unread email."
        else:
            return f"📫 You have {unread_count} unread emails."
        
    except Exception as e:
        return f"Error checking unread emails: {str(e)}"
