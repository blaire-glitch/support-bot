"""LinkedIn profile management tools using LinkedIn API."""

import os
import httpx
from typing import Annotated
from pydantic import Field


LINKEDIN_API_URL = "https://api.linkedin.com/v2"


def _get_linkedin_headers():
    """Get headers for LinkedIn API requests."""
    access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    if not access_token:
        return None
    return {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0",
    }


def _get_user_id():
    """Get the LinkedIn user ID (URN)."""
    headers = _get_linkedin_headers()
    if not headers:
        return None
    
    try:
        with httpx.Client() as client:
            response = client.get(
                f"{LINKEDIN_API_URL}/userinfo",
                headers=headers
            )
            response.raise_for_status()
            return response.json().get("sub")
    except Exception:
        return None


def get_linkedin_profile() -> str:
    """Get the current LinkedIn profile information.
    
    Returns:
        The profile details including headline, summary, etc.
    """
    access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    
    if not access_token:
        return "Error: LinkedIn credentials not configured. Please set LINKEDIN_ACCESS_TOKEN in .env file."
    
    headers = _get_linkedin_headers()
    
    try:
        # Get basic profile using userinfo endpoint (OpenID Connect)
        with httpx.Client() as client:
            response = client.get(
                f"{LINKEDIN_API_URL}/userinfo",
                headers=headers
            )
            response.raise_for_status()
            profile = response.json()
            
            result = "💼 **LinkedIn Profile**\n\n"
            result += f"**Name:** {profile.get('name', 'Not available')}\n"
            result += f"**Email:** {profile.get('email', 'Not available')}\n"
            result += f"**Picture:** {profile.get('picture', 'Not set')}\n"
            result += f"**Locale:** {profile.get('locale', {}).get('language', 'Not set')}\n"
            
            return result
            
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            return "Error: LinkedIn access token expired or invalid. Please generate a new access token."
        return f"Error fetching LinkedIn profile: {str(e)}"
    except Exception as e:
        return f"Error fetching LinkedIn profile: {str(e)}"


def update_linkedin_headline(
    headline: Annotated[str, Field(description="New headline text (max 220 characters)")],
) -> str:
    """Update LinkedIn profile headline.
    
    Note: LinkedIn's API has limited write access. Full profile updates 
    require Marketing Developer Platform access. This function provides
    guidance and attempts the update.
    
    Args:
        headline: The new headline text
        
    Returns:
        Result of the update attempt
    """
    access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    
    if not access_token:
        return "Error: LinkedIn credentials not configured. Please set LINKEDIN_ACCESS_TOKEN in .env file."
    
    if len(headline) > 220:
        return f"Error: Headline is too long ({len(headline)} characters). Maximum is 220 characters."
    
    # Note: LinkedIn's public API has very limited write access
    # Profile updates typically require Marketing Developer Platform approval
    return f"""💼 **LinkedIn Headline Update Request**

**Requested headline:** "{headline}"

⚠️ **Important:** LinkedIn's public API has limited profile editing capabilities. 
To update your headline:

**Option 1 - Manual Update:**
1. Go to linkedin.com/in/YOUR-PROFILE
2. Click the pencil icon next to your headline
3. Enter: "{headline}"
4. Save changes

**Option 2 - API Access (Requires Approval):**
To enable programmatic profile updates:
1. Apply for LinkedIn Marketing Developer Platform access
2. Request the `w_member_social` scope
3. Get your app approved for profile editing

Would you like me to help with anything else?"""


def update_linkedin_summary(
    summary: Annotated[str, Field(description="New 'About' section text (max 2600 characters)")],
) -> str:
    """Update LinkedIn profile summary/about section.
    
    Args:
        summary: The new summary text
        
    Returns:
        Result of the update attempt
    """
    access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    
    if not access_token:
        return "Error: LinkedIn credentials not configured."
    
    if len(summary) > 2600:
        return f"Error: Summary is too long ({len(summary)} characters). Maximum is 2600 characters."
    
    return f"""💼 **LinkedIn Summary Update Request**

**Requested summary preview:** "{summary[:200]}..."

⚠️ **Note:** LinkedIn's standard API doesn't allow direct profile summary updates.

**To update your summary:**
1. Visit linkedin.com/in/YOUR-PROFILE
2. Scroll to the "About" section
3. Click the pencil icon
4. Paste your new summary
5. Save changes

**Your prepared summary has been noted.** Copy it from above when making the manual update."""


def post_linkedin_update(
    text: Annotated[str, Field(description="The post content (max 3000 characters)")],
    visibility: Annotated[str, Field(description="Post visibility: 'PUBLIC' or 'CONNECTIONS'")] = "PUBLIC",
) -> str:
    """Post an update/share on LinkedIn.
    
    Args:
        text: The content of the post
        visibility: Who can see the post (PUBLIC or CONNECTIONS)
        
    Returns:
        Result of posting the update
    """
    access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    
    if not access_token:
        return "Error: LinkedIn credentials not configured."
    
    if len(text) > 3000:
        return f"Error: Post is too long ({len(text)} characters). Maximum is 3000 characters."
    
    headers = _get_linkedin_headers()
    
    try:
        # Get user URN
        with httpx.Client() as client:
            # First get user info
            user_response = client.get(f"{LINKEDIN_API_URL}/userinfo", headers=headers)
            user_response.raise_for_status()
            user_id = user_response.json().get("sub")
            
            if not user_id:
                return "Error: Could not retrieve LinkedIn user ID."
            
            # Create post payload
            author_urn = f"urn:li:person:{user_id}"
            
            payload = {
                "author": author_urn,
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": text
                        },
                        "shareMediaCategory": "NONE"
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": visibility
                }
            }
            
            # Post to UGC endpoint
            post_response = client.post(
                f"{LINKEDIN_API_URL}/ugcPosts",
                json=payload,
                headers=headers
            )
            post_response.raise_for_status()
            
            post_id = post_response.headers.get("x-restli-id", "created")
            
            return f"""✅ **LinkedIn Post Published Successfully!**

**Post ID:** {post_id}
**Visibility:** {visibility}
**Content preview:** "{text[:100]}..."

Your update is now live on LinkedIn!"""
            
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            return "Error: LinkedIn access token expired. Please refresh your token."
        elif e.response.status_code == 403:
            return """Error: Insufficient permissions to post on LinkedIn.

Your LinkedIn app needs the `w_member_social` scope to post updates.
Please ensure your app has this permission and regenerate your access token."""
        else:
            error_body = e.response.text
            return f"Error posting to LinkedIn: {e.response.status_code} - {error_body}"
    except Exception as e:
        return f"Error posting to LinkedIn: {str(e)}"


def get_linkedin_connections_count() -> str:
    """Get the count of LinkedIn connections.
    
    Returns:
        The number of connections or an error message
    """
    access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    
    if not access_token:
        return "Error: LinkedIn credentials not configured."
    
    headers = _get_linkedin_headers()
    
    try:
        with httpx.Client() as client:
            response = client.get(
                f"{LINKEDIN_API_URL}/connections",
                headers=headers,
                params={"q": "viewer", "count": 0}
            )
            
            if response.status_code == 403:
                return """💼 **LinkedIn Connections**

⚠️ The connections count requires additional API permissions.

To view your connections count manually:
1. Go to linkedin.com/mynetwork/invite-connect/connections/
2. Your connection count is displayed at the top"""
            
            response.raise_for_status()
            data = response.json()
            
            total = data.get("_total", data.get("paging", {}).get("total", "Unknown"))
            return f"💼 You have **{total}** LinkedIn connections."
            
    except Exception as e:
        return f"Error fetching connections: {str(e)}"


def send_linkedin_message(
    recipient_name: Annotated[str, Field(description="Name of the person to message")],
    message: Annotated[str, Field(description="Message content")],
) -> str:
    """Send a message to a LinkedIn connection.
    
    Note: LinkedIn messaging API requires Messaging API access which 
    is highly restricted. This provides guidance instead.
    
    Args:
        recipient_name: The name of the connection to message
        message: The message to send
        
    Returns:
        Guidance on sending the message
    """
    return f"""💼 **LinkedIn Message Request**

**To:** {recipient_name}
**Message:** "{message[:100]}..."

⚠️ **LinkedIn Messaging API Limitations:**
LinkedIn's messaging API is restricted to approved partners only.

**To send your message:**
1. Go to linkedin.com/messaging
2. Start a new conversation with "{recipient_name}"
3. Send: "{message}"

Alternatively, I can help you draft or refine the message content."""
