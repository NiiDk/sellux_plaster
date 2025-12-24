"""
Forms for account registration and profile updates.

We extend Django's `UserCreationForm` to include additional fields for our
custom user model, and provide a `ModelForm` for updating profile fields.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    """Registration form for `CustomUser`.

    Includes email and optional profile fields. Password validation is
    handled by `UserCreationForm`.
    """

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone')


class ProfileUpdateForm(forms.ModelForm):
    """Form to update profile fields for the logged-in user."""

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'bio', 'profile_image')
