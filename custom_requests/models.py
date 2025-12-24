from django.db import models
from django.conf import settings
from decimal import Decimal

class CustomRequest(models.Model):
    SERVICE_TYPES = [
        ('pop_ceiling', 'POP Ceiling Design'),
        ('cornice_install', 'Cornice Installation'),
        ('drywall_partition', 'Drywall/Partitioning'),
        ('skimming', 'Skimming & Finishing'),
        ('custom_furniture', 'Custom Joinery/Furniture'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('quoted', 'Quote Sent'),
        ('accepted', 'Accepted & Awaiting Payment'),
        ('paid', 'Paid & Scheduled'),
        ('rejected', 'Declined'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project_title = models.CharField(max_length=200)
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPES, default='pop_ceiling')
    estimated_area = models.DecimalField(max_digits=10, decimal_places=2, help_text="Estimated area in square feet", null=True, blank=True)
    description = models.TextField()
    
    inspiration_image = models.ImageField(upload_to='custom_requests/inspiration/', blank=True, null=True)
    site_photo = models.ImageField(upload_to='custom_requests/sites/', blank=True, null=True)
    
    # Admin Fields
    quoted_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    admin_note = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Link to final order
    order = models.OneToOneField('orders.Order', on_delete=models.SET_NULL, null=True, blank=True, related_name='custom_project')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Mark as quoted if price is added by admin
        if self.quoted_price > 0 and self.status == 'pending':
            self.status = 'quoted'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.project_title} ({self.get_status_display()})"
