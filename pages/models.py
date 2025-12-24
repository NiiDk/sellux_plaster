from django.db import models

class StaticPage(models.Model):
    slug = models.SlugField(max_length=50, unique=True)
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Testimonial(models.Model):
    client_name = models.CharField(max_length=100)
    client_title = models.CharField(max_length=100, blank=True, help_text="e.g. Homeowner, Architect")
    content = models.TextField()
    rating = models.PositiveIntegerField(default=5)
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    is_featured = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Testimonial from {self.client_name}"
