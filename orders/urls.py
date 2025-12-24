from django.urls import path
from .views import OrderCreateView, OrderSuccessView

app_name = 'orders'

urlpatterns = [
    path('create/', OrderCreateView.as_view(), name='order_create'),
    path('success/<int:pk>/', OrderSuccessView.as_view(), name='success'),
]
