"""
Custom user model extending AbstractUser to include optional profile fields.

Extending `AbstractUser` preserves Django's authentication behavior while
allowing project-specific profile fields (phone, bio, profile_image).
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    # Optional phone number for two-factor or contact
    phone = models.CharField(max_length=30, blank=True)

    # Profile image stored in MEDIA_ROOT/profiles/
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)

    # Small bio for the user's profile page
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.username
