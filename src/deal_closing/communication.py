"""
Communication Manager for Deal Closing
This module handles all communications with prospects.
"""

import os
import logging
import json
from datetime import datetime
from jinja2 import Template

logger = logging.getLogger(__name__)

class CommunicationManager:
    """Manages communications with prospects."""
    
    def __init__(self, sendgrid_api_key, templates):
        """Initialize the Communication Manager."""
        self.sendgrid_api_key = sendgrid_api_key
        self.templates = templates
        logger.info("Initialized Communication Manager")
    
    def send_email(self, template_id, recipient_email, template_vars, attachments=None):
        """Send an email using a template."""
        logger.info(f"Sending email with template {template_id} to {recipient_email}")
        
        try:
            # Find the template
            template_data = self._get_template(template_id)
            
            if not template_data:
                logger.error(f"Template {template_id} not found")
                return None
            
            # Render the template
            subject = self._render_template_string(template_data.get("subject", ""), template_vars)
            body = self._render_template_string(template_data.get("body", ""), template_vars)
            
            # In a real implementation, this would use SendGrid API
            # For this demo, we'll simulate sending
            message_id = self._simulate_send_email(recipient_email, subject, body, attachments)
            
            logger.info(f"Email sent successfully. Message ID: {message_id}")
            return message_id
        
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return None
    
    def _get_template(self, template_id):
        """Get a template by ID."""
        for template in self.templates:
            if template.get("id") == template_id:
                return template
        return None
    
    def _render_template_string(self, template_string, template_vars):
        """Render a template string with variables."""
        template = Template(template_string)
        return template.render(**template_vars)
    
    def get_rendered_template(self, template_id, template_vars):
        """Get a rendered template for recording purposes."""
        template_data = self._get_template(template_id)
        
        if not template_data:
            return ""
        
        subject = self._render_template_string(template_data.get("subject", ""), template_vars)
        body = self._render_template_string(template_data.get("body", ""), template_vars)
        
        return f"Subject: {subject}\n\n{body}"
    
    def _simulate_send_email(self, recipient_email, subject, body, attachments=None):
        """Simulate sending an email (for demo purposes)."""
        # Generate a random message ID
        import random
        import string
        message_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        
        # Log the email details
        logger.info(f"SIMULATED EMAIL:")
        logger.info(f"To: {recipient_email}")
        logger.info(f"Subject: {subject}")
        logger.info(f"Body: {body[:100]}...")
        
        if attachments:
            logger.info(f"Attachments: {attachments}")
        
        return message_id
