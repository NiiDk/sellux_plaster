from django import forms


class CatalogueFilterForm(forms.Form):
    category = forms.CharField(required=False)
    price_min = forms.DecimalField(required=False, decimal_places=2, max_digits=10)
    price_max = forms.DecimalField(required=False, decimal_places=2, max_digits=10)
