"""Tests for Support Bot tools."""

import pytest
import os


class TestEmailTools:
    """Tests for email tools."""
    
    def test_send_email_no_credentials(self):
        """Test send_email when credentials are not configured."""
        # Temporarily clear env vars
        original_email = os.environ.get("EMAIL_ADDRESS")
        original_password = os.environ.get("EMAIL_PASSWORD")
        
        os.environ.pop("EMAIL_ADDRESS", None)
        os.environ.pop("EMAIL_PASSWORD", None)
        
        from support_bot.tools.email_tools import send_email
        
        result = send_email(
            to="test@example.com",
            subject="Test",
            body="Test body"
        )
        
        assert "Error" in result
        assert "credentials not configured" in result
        
        # Restore
        if original_email:
            os.environ["EMAIL_ADDRESS"] = original_email
        if original_password:
            os.environ["EMAIL_PASSWORD"] = original_password
    
    def test_get_unread_count_no_credentials(self):
        """Test get_unread_count when credentials are not configured."""
        os.environ.pop("EMAIL_ADDRESS", None)
        os.environ.pop("EMAIL_PASSWORD", None)
        
        from support_bot.tools.email_tools import get_unread_count
        
        result = get_unread_count()
        assert "Error" in result


class TestWhatsAppTools:
    """Tests for WhatsApp tools."""
    
    def test_send_message_no_credentials(self):
        """Test send_whatsapp_message when credentials are not configured."""
        os.environ.pop("WHATSAPP_PHONE_NUMBER_ID", None)
        os.environ.pop("WHATSAPP_ACCESS_TOKEN", None)
        
        from support_bot.tools.whatsapp_tools import send_whatsapp_message
        
        result = send_whatsapp_message(
            phone_number="+1234567890",
            message="Test message"
        )
        
        assert "Error" in result
        assert "credentials not configured" in result
    
    def test_get_messages_returns_guidance(self):
        """Test that get_whatsapp_messages returns webhook guidance."""
        from support_bot.tools.whatsapp_tools import get_whatsapp_messages
        
        # Even without credentials, should return guidance
        os.environ["WHATSAPP_PHONE_NUMBER_ID"] = "test"
        os.environ["WHATSAPP_ACCESS_TOKEN"] = "test"
        
        result = get_whatsapp_messages()
        
        assert "webhook" in result.lower()
        
        # Cleanup
        os.environ.pop("WHATSAPP_PHONE_NUMBER_ID", None)
        os.environ.pop("WHATSAPP_ACCESS_TOKEN", None)


class TestLinkedInTools:
    """Tests for LinkedIn tools."""
    
    def test_get_profile_no_credentials(self):
        """Test get_linkedin_profile when credentials are not configured."""
        os.environ.pop("LINKEDIN_ACCESS_TOKEN", None)
        
        from support_bot.tools.linkedin_tools import get_linkedin_profile
        
        result = get_linkedin_profile()
        
        assert "Error" in result
        assert "credentials not configured" in result
    
    def test_headline_too_long(self):
        """Test update_linkedin_headline with too long text."""
        os.environ["LINKEDIN_ACCESS_TOKEN"] = "test_token"
        
        from support_bot.tools.linkedin_tools import update_linkedin_headline
        
        long_headline = "A" * 250  # Over 220 char limit
        result = update_linkedin_headline(headline=long_headline)
        
        assert "too long" in result
        
        os.environ.pop("LINKEDIN_ACCESS_TOKEN", None)
    
    def test_summary_too_long(self):
        """Test update_linkedin_summary with too long text."""
        os.environ["LINKEDIN_ACCESS_TOKEN"] = "test_token"
        
        from support_bot.tools.linkedin_tools import update_linkedin_summary
        
        long_summary = "A" * 3000  # Over 2600 char limit
        result = update_linkedin_summary(summary=long_summary)
        
        assert "too long" in result
        
        os.environ.pop("LINKEDIN_ACCESS_TOKEN", None)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
