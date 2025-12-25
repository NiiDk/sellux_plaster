import requests
import logging
import hmac
import hashlib
import os
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
        logger.info(f"SMS trigger: To {phone_number} -> {message}")
        return True

class AIService(BaseService):
    """
    Architectural AI Service for Sellux Plaster.
    Can be linked to OpenAI, Anthropic, or Gemini.
    """
    API_KEY = os.getenv('AI_API_KEY')
    API_URL = "https://api.openai.com/v1/chat/completions"

    @classmethod
    def enhance_design_brief(cls, raw_description, service_type):
        """
        Transforms a simple user description into a professional architectural brief.
        """
        if not cls.API_KEY:
            return f"Service: {service_type}. Note: {raw_description} (AI enhancement disabled - missing key)"

        prompt = f"Act as an architectural designer for Sellux Plaster. Enhance this brief for a {service_type}: '{raw_description}'. Use professional terminology like 'recessed lighting', 'shadow gaps', or 'crown moldings'. Keep it concise but luxury-focused."
        
        try:
            headers = {"Authorization": f"Bearer {cls.API_KEY}", "Content-Type": "application/json"}
            data = {
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": prompt}]
            }
            response = requests.post(cls.API_URL, headers=headers, json=data, timeout=10)
            return response.json()['choices'][0]['message']['content']
        except Exception as e:
            logger.error(f"AI brief enhancement failed: {str(e)}")
            return raw_description

    @classmethod
    def suggest_quote_price(cls, service_type, sq_ft):
        """
        Provides a baseline estimate for the admin based on Ghanian market rates.
        """
        rates = {
            'pop_ceiling': 45, # GH₵ per sq ft
            'cornice_install': 15, 
            'drywall_partition': 65,
            'skimming': 12
        }
        base_rate = rates.get(service_type, 20)
        estimated = float(sq_ft or 0) * base_rate
        return round(estimated, 2)
