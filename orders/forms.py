from django import forms
from .models import Order
from shipping.models import City

class OrderCreateForm(forms.ModelForm):
    city = forms.ModelChoiceField(queryset=City.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'delivery_option', 'address', 'city']
        widgets = {
            'delivery_option': forms.RadioSelect
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(OrderCreateForm, self).__init__(*args, **kwargs)
        if user and user.is_authenticated:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if not phone_number.startswith(('+233', '0')) or not phone_number.replace('+', '').isdigit() or not (10 <= len(phone_number) <= 13):
            raise forms.ValidationError('Please enter a valid Ghanaian phone number.')
        return phone_number

    def clean(self):
        cleaned_data = super().clean()
        delivery_option = cleaned_data.get('delivery_option')
        if delivery_option == Order.DELIVERY_OPTION_DELIVERY:
            if not cleaned_data.get('address'):
                self.add_error('address', 'This field is required for delivery.')
            if not cleaned_data.get('city'):
                self.add_error('city', 'This field is required for delivery.')
        return cleaned_data
