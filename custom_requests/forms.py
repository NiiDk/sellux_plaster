from django import forms
from .models import CustomRequest

class CustomRequestForm(forms.ModelForm):
    class Meta:
        model = CustomRequest
        fields = ['project_title', 'description', 'inspiration_image', 'site_photo']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell us about your space, dimensions, and the style you want...'}),
        }
