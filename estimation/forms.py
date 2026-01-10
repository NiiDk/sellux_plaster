from django import forms
from .models import Service

class EstimationForm(forms.Form):
    service = forms.ModelChoiceField(
        queryset=Service.objects.filter(is_active=True),
        empty_label="-- Select a Service --",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    area = forms.DecimalField(
        min_value=1,
        label="Area (in square metres)",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 25'})
    )
