from django import forms
from .models import CustomRequest

class CustomRequestForm(forms.ModelForm):
    class Meta:
        model = CustomRequest
        fields = ['project_title', 'service_type', 'estimated_area', 'description', 'inspiration_image', 'site_photo']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Detailed description of the architectural style and specific requirements...'}),
            'estimated_area': forms.NumberInput(attrs={'placeholder': 'Total square feet (approx)'}),
        }
