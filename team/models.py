from django.db import models
from django.urls import reverse

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class TeamMember(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    job_title = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    bio = models.TextField()
    specialization = models.CharField(max_length=200, help_text="e.g., Tax Law, International Audit")
    qualifications = models.TextField(help_text="List of professional designations (e.g., ICAG, MBA)")
    linkedin_url = models.URLField(blank=True)
    profile_image = models.ImageField(upload_to='team/')
    order_weight = models.PositiveIntegerField(default=10, help_text="Lower values appear first (Managing Partners = 1)")
    is_active = models.BooleanField(default=True)
    is_management = models.BooleanField(default=False, help_text="Check this for members of the Firm Leadership team.")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_absolute_url(self):
        return reverse('team:team_detail', args=[self.id])

    class Meta:
        ordering = ['order_weight', 'first_name']
