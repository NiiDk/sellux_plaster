from django.urls import path
from .views import ContactView, ContactSuccessView

app_name = 'contact'

urlpatterns = [
    path('', ContactView.as_view(), name='contact_us'),
    path('success/', ContactSuccessView.as_view(), name='success'),
]
