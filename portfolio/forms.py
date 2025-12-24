from django import forms


class PortfolioFilterForm(forms.Form):
    category = forms.CharField(required=False, label='Category')
    year = forms.IntegerField(required=False, label='Year')
