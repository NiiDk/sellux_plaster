from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from core.services import NotificationService

@receiver(post_save, sender=Order)
def notify_order_status_change(sender, instance, created, **kwargs):
    """
    Triggers notifications when an order is created or its status is updated.
    """
    if created:
        # 1. New Order Confirmation
        subject = f"Order Confirmation #{instance.id} - Sellux Plaster"
        template = 'emails/order_confirmation.html'
        NotificationService.send_email(
            subject=subject,
            recipient_list=[instance.email],
            template_name=template,
            context={'order': instance}
        )
    else:
        # 2. Status Updates (e.g. Shipped, Paid)
        if instance.payment_status == 'paid':
            NotificationService.send_sms(
                phone_number=instance.user.phone, 
                message=f"Payment received for Order #{instance.id}. We are processing your luxury finishes!"
            )
