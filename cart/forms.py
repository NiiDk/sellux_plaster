from django import forms

class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control text-center', 'value': 1})
    )
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
