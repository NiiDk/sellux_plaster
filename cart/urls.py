from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('clear/', views.cart_clear, name='cart_clear'),
]
