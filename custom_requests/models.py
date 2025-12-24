from django.db import models
from django.conf import settings

class CustomRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('quoted', 'Quote Sent'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project_title = models.CharField(max_length=200, help_text="e.g. Master Bedroom POP Ceiling")
    description = models.TextField(help_text="Describe your vision or the dimensions of the space.")
    inspiration_image = models.ImageField(upload_to='custom_requests/inspiration/', blank=True, null=True)
    site_photo = models.ImageField(upload_to='custom_requests/sites/', blank=True, null=True, help_text="Photo of the current wall/ceiling.")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    admin_note = models.TextField(blank=True, help_text="Notes from the Sellux team. Adding a note will mark this as 'Quote Sent'.")

    def save(self, *args, **kwargs):
        # Automatically update status to 'quoted' if an admin note is added to a pending request
        if self.admin_note and self.status == 'pending':
            self.status = 'quoted'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.project_title} - {self.user.username}"
