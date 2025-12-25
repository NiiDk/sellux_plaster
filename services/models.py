from django.db import models
from django.urls import reverse

class Service(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, help_text="Bootstrap icon class name (e.g., bi-layers)")
    short_description = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='services/')
    
    # Contextual Selling: Recommended products for this specific service
    recommended_products = models.ManyToManyField(
        'catalogue.Product', 
        blank=True, 
        related_name='suggested_for_services',
        help_text="Select materials from the catalogue usually required for this service."
    )
    
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('services:service_detail', args=[self.slug])
