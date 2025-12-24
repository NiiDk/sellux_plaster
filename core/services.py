import requests
import logging
import hmac
import hashlib
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

logger = logging.getLogger(__name__)

class BaseService:
    """Base class for external integrations."""
    pass

class PaystackService(BaseService):
    """
    Service layer for Paystack API interactions.
    """
    BASE_URL = "https://api.paystack.co"

    @classmethod
    def get_headers(cls):
        return {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }

    @classmethod
    def initialize_transaction(cls, email, amount_in_cedis, callback_url, metadata=None):
        url = f"{cls.BASE_URL}/transaction/initialize"
        amount = int(float(amount_in_cedis) * 100)
        
        payload = {
            "email": email,
            "amount": amount,
            "currency": "GHS",
            "callback_url": callback_url,
            "metadata": metadata or {}
        }
        
        try:
            response = requests.post(url, headers=cls.get_headers(), json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Paystack initialization failed: {str(e)}")
            return None

    @classmethod
    def verify_payment(cls, reference):
        url = f"{cls.BASE_URL}/transaction/verify/{reference}"
        try:
            response = requests.get(url, headers=cls.get_headers())
            response.raise_for_status()
            data = response.json()
            if data['status'] and data['data']['status'] == 'success':
                return True, data['data']
            return False, data.get('message', 'Verification failed')
        except requests.exceptions.RequestException as e:
            logger.error(f"Paystack verification failed: {str(e)}")
            return False, str(e)

    @classmethod
    def verify_webhook(cls, payload, signature):
        secret = settings.PAYSTACK_SECRET_KEY.encode('utf-8')
        computed_hmac = hmac.new(secret, payload, hashlib.sha512).hexdigest()
        return computed_hmac == signature

class NotificationService(BaseService):
    """
    Unified service for sending Emails and SMS.
    """
    @classmethod
    def send_email(cls, subject, recipient_list, template_name, context):
        """
        Sends a branded HTML email.
        """
        html_content = render_to_string(template_name, context)
        text_content = strip_tags(html_content)
        
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=recipient_list
        )
        email.attach_alternative(html_content, "text/html")
        
        try:
            email.send()
            return True
        except Exception as e:
            logger.error(f"Failed to send email to {recipient_list}: {str(e)}")
            return False

    @classmethod
    def send_sms(cls, phone_number, message):
        """
        Placeholder for Twilio/BulkSMS integration.
        """
        logger.info(f"SMS trigger: To {phone_number} -> {message}")
        # Implementation for Twilio would go here
        return True

class AIService(BaseService):
    """ Hook for future AI integrations. """
    @classmethod
    def generate_content(cls, prompt):
        return "AI content generation hook active."
