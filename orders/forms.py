from django import forms
from django.core.exceptions import ValidationError
from catalogue.models import Product

class OrderForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.filter(is_available=True), widget=forms.HiddenInput)
    quantity = forms.IntegerField(min_value=1, initial=1)

    def clean_product(self):
        product = self.cleaned_data['product']
        if product.stock <= 0:
            raise ValidationError('This product is out of stock.')
        return product
