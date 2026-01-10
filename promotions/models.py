from django.db import models

class Promotion(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='promotions/', help_text="Image for the left side of the popup.")
    is_active = models.BooleanField(default=False, help_text="Only one promotion can be active at a time.")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.is_active:
            # Ensure only one promotion is active at a time
            Promotion.objects.filter(is_active=True).update(is_active=False)
        super(Promotion, self).save(*args, **kwargs)

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
