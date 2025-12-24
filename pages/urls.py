from django.urls import path
from .views import (
    HomeView, AboutView, TermsView, PrivacyView,
    RefundView, ShippingView, global_search
)

app_name = 'pages'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('terms/', TermsView.as_view(), name='terms'),
    path('privacy/', PrivacyView.as_view(), name='privacy'),
    path('refund-policy/', RefundView.as_view(), name='refund'),
    path('shipping-policy/', ShippingView.as_view(), name='shipping'),
    path('search/', global_search, name='global_search'),
]
