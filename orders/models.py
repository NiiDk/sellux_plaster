from decimal import Decimal
from django.conf import settings
from django.db import models
from django.urls import reverse
from catalogue.models import Product

class Order(models.Model):
    DELIVERY_OPTION_DELIVERY = 'delivery'
    DELIVERY_OPTION_PICKUP = 'pickup'

    DELIVERY_CHOICES = [
        (DELIVERY_OPTION_DELIVERY, 'Delivery'),
        (DELIVERY_OPTION_PICKUP, 'In-store Pickup'),
    ]

    STATUS_PENDING = 'pending'
    STATUS_PROCESSING = 'processing'
    STATUS_SHIPPED = 'shipped'
    STATUS_DELIVERED = 'delivered'
    STATUS_CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_PROCESSING, 'Processing'),
        (STATUS_SHIPPED, 'Shipped'),
        (STATUS_DELIVERED, 'Delivered'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]

    PAYMENT_PENDING = 'pending'
    PAYMENT_PAID = 'paid'
    PAYMENT_FAILED = 'failed'
    
    PAYMENT_CHOICES = [
        (PAYMENT_PENDING, 'Pending'),
        (PAYMENT_PAID, 'Paid'),
        (PAYMENT_FAILED, 'Failed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15, blank=True)
    delivery_option = models.CharField(max_length=20, choices=DELIVERY_CHOICES, default=DELIVERY_OPTION_DELIVERY)
    street_address = models.CharField(max_length=250, blank=True, help_text="e.g., 123 Osu Street")
    building_number = models.CharField(max_length=50, blank=True, help_text="House/Building number")
    region = models.CharField(max_length=100, blank=True, help_text="Region/District")
    postal_code = models.CharField(max_length=20, blank=True, help_text="Postal or ZIP code")
    address = models.CharField(max_length=250, blank=True)  # Keep for backward compatibility
    city = models.CharField(max_length=100, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default=PAYMENT_PENDING)
    
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    # Financial Metadata
    paystack_ref = models.CharField(max_length=100, blank=True, unique=True, null=True)
    payment_channel = models.CharField(max_length=50, blank=True, help_text="e.g. mobile_money, card")
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    
    admin_feedback = models.TextField(blank=True, help_text="Notes for the customer regarding order status.")
    
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} - {self.first_name}"

    def get_grand_total(self):
        return self.total_amount + self.tax + self.delivery_fee

    def get_absolute_url(self):
        return reverse('orders:success', kwargs={'pk': self.pk})

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Item {self.id} for Order {self.order.id}"

    def get_cost(self):
        return self.price * self.quantity
