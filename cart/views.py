from django.shortcuts import redirect
from .cart import Cart

def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect('catalogue:product_list')
