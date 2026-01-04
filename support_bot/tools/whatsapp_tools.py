"""WhatsApp messaging tools using WhatsApp Business API."""

import os
import httpx
from typing import Annotated
from pydantic import Field


WHATSAPP_API_URL = "https://graph.facebook.com/v18.0"


def send_whatsapp_message(
    phone_number: Annotated[str, Field(description="Recipient phone number with country code (e.g., +1234567890)")],
    message: Annotated[str, Field(description="The message content to send")],
) -> str:
    """Send a WhatsApp message to the specified phone number.
    
    Args:
        phone_number: The recipient's phone number with country code
        message: The text message to send
        
    Returns:
        A confirmation message with the result
    """
    phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
    access_token = os.getenv("WHATSAPP_ACCESS_TOKEN")
    
    if not phone_number_id or not access_token:
        return "Error: WhatsApp credentials not configured. Please set WHATSAPP_PHONE_NUMBER_ID and WHATSAPP_ACCESS_TOKEN in .env file."
    
    # Clean phone number (remove + and spaces)
    clean_number = phone_number.replace("+", "").replace(" ", "").replace("-", "")
    
    try:
        url = f"{WHATSAPP_API_URL}/{phone_number_id}/messages"
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": clean_number,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": message
            }
        }
        
        with httpx.Client() as client:
            response = client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            message_id = result.get("messages", [{}])[0].get("id", "unknown")
            
            return f"✅ WhatsApp message sent successfully to {phone_number}\nMessage ID: {message_id}"
            
    except httpx.HTTPStatusError as e:
        error_data = e.response.json() if e.response.content else {}
        error_message = error_data.get("error", {}).get("message", str(e))
        return f"Error sending WhatsApp message: {error_message}"
    except Exception as e:
        return f"Error sending WhatsApp message: {str(e)}"


def send_whatsapp_template_message(
    phone_number: Annotated[str, Field(description="Recipient phone number with country code")],
    template_name: Annotated[str, Field(description="Name of the approved message template")],
    language_code: Annotated[str, Field(description="Language code (e.g., 'en_US')")] = "en_US",
) -> str:
    """Send a WhatsApp template message (for business notifications).
    
    Args:
        phone_number: The recipient's phone number with country code
        template_name: The name of the pre-approved template
        language_code: The language code for the template
        
    Returns:
        A confirmation message with the result
    """
    phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
    access_token = os.getenv("WHATSAPP_ACCESS_TOKEN")
    
    if not phone_number_id or not access_token:
        return "Error: WhatsApp credentials not configured."
    
    clean_number = phone_number.replace("+", "").replace(" ", "").replace("-", "")
    
    try:
        url = f"{WHATSAPP_API_URL}/{phone_number_id}/messages"
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "messaging_product": "whatsapp",
            "to": clean_number,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {
                    "code": language_code
                }
            }
        }
        
        with httpx.Client() as client:
            response = client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            
            return f"✅ WhatsApp template message '{template_name}' sent to {phone_number}"
            
    except httpx.HTTPStatusError as e:
        error_data = e.response.json() if e.response.content else {}
        error_message = error_data.get("error", {}).get("message", str(e))
        return f"Error sending template message: {error_message}"
    except Exception as e:
        return f"Error sending template message: {str(e)}"


def get_whatsapp_messages(
    count: Annotated[int, Field(description="Number of recent messages to retrieve")] = 10,
) -> str:
    """Get recent WhatsApp messages/conversations.
    
    Note: This requires webhook setup for real-time messages. 
    This function provides guidance on setting up message retrieval.
    
    Args:
        count: Number of messages to retrieve
        
    Returns:
        Information about message retrieval or stored messages
    """
    phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
    access_token = os.getenv("WHATSAPP_ACCESS_TOKEN")
    
    if not phone_number_id or not access_token:
        return "Error: WhatsApp credentials not configured."
    
    # Note: WhatsApp Business API uses webhooks for incoming messages
    # Real-time message retrieval requires a webhook server
    return """📱 **WhatsApp Message Retrieval**

The WhatsApp Business API uses webhooks for incoming messages. To receive messages:

1. **Set up a webhook server** to receive incoming message notifications
2. **Configure the webhook URL** in your Meta Business Dashboard
3. **Store messages** in a database when received via webhook

Currently, the WhatsApp Business API does not provide a direct endpoint to 
fetch message history. Messages must be captured in real-time via webhooks.

For a complete solution, consider:
- Setting up a webhook endpoint (e.g., using Flask/FastAPI)
- Storing messages in a database (SQLite, PostgreSQL, etc.)
- Querying your database for message history

Would you like help setting up a webhook server for WhatsApp messages?"""


def get_whatsapp_business_profile() -> str:
    """Get the WhatsApp Business profile information.
    
    Returns:
        The business profile details
    """
    phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
    access_token = os.getenv("WHATSAPP_ACCESS_TOKEN")
    
    if not phone_number_id or not access_token:
        return "Error: WhatsApp credentials not configured."
    
    try:
        url = f"{WHATSAPP_API_URL}/{phone_number_id}/whatsapp_business_profile"
        params = {
            "fields": "about,address,description,email,profile_picture_url,websites,vertical"
        }
        
        headers = {
            "Authorization": f"Bearer {access_token}",
        }
        
        with httpx.Client() as client:
            response = client.get(url, params=params, headers=headers)
            response.raise_for_status()
            
            profile = response.json().get("data", [{}])[0]
            
            result = "📱 **WhatsApp Business Profile**\n\n"
            result += f"**About:** {profile.get('about', 'Not set')}\n"
            result += f"**Description:** {profile.get('description', 'Not set')}\n"
            result += f"**Email:** {profile.get('email', 'Not set')}\n"
            result += f"**Address:** {profile.get('address', 'Not set')}\n"
            result += f"**Industry:** {profile.get('vertical', 'Not set')}\n"
            
            websites = profile.get('websites', [])
            if websites:
                result += f"**Websites:** {', '.join(websites)}\n"
            
            return result
            
    except httpx.HTTPStatusError as e:
        error_data = e.response.json() if e.response.content else {}
        error_message = error_data.get("error", {}).get("message", str(e))
        return f"Error fetching business profile: {error_message}"
    except Exception as e:
        return f"Error fetching business profile: {str(e)}"
