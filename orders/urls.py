from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.OrderCreateView.as_view(), name='order_create'),
    path('verify/', views.OrderVerifyView.as_view(), name='verify'),
    path('webhook/', views.paystack_webhook, name='webhook'),
    path('success/<int:pk>/', views.OrderSuccessView.as_view(), name='success'),
]
