import json
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib import messages

from .models import Order, OrderItem
from cart.cart import Cart
from catalogue.models import Product
from core.services import PaystackService

class OrderCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'orders/order_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = Cart(self.request)
        return context

    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        product_id = request.GET.get('product')
        quantity = int(request.GET.get('quantity', 1))

        if product_id:
            product = get_object_or_404(Product, id=product_id)
            cart.add(product=product, quantity=quantity)
            return redirect('orders:order_create')

        if len(cart) == 0:
            messages.warning(request, "Your cart is empty. Please add items before checking out.")
            return redirect('catalogue:product_list')
            
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        if len(cart) == 0:
            return redirect('catalogue:product_list')

        # Create Order
        order = Order.objects.create(
            user=request.user,
            first_name=request.user.first_name or request.user.username,
            last_name=request.user.last_name or "Client",
            email=request.user.email,
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            total_amount=cart.get_total_price()
        )
        
        # Create Order Items
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity']
            )
        
        # Initialize Paystack
        callback_url = request.build_absolute_uri(reverse('orders:verify'))
        res = PaystackService.initialize_transaction(
            email=order.email,
            amount_in_cedis=order.total_amount,
            callback_url=callback_url,
            metadata={'order_id': order.id}
        )
        
        if res and res['status']:
            order.paystack_ref = res['data']['reference']
            order.save()
            cart.clear()
            return redirect(res['data']['authorization_url'])
        
        return self.render_to_response(self.get_context_data(error='Payment initialization failed'))

class OrderVerifyView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        reference = request.GET.get('reference')
        success, data = PaystackService.verify_payment(reference)
        
        if success:
            order_id = data['metadata']['order_id']
            order = get_object_or_404(Order, id=order_id)
            order.payment_status = 'paid'
            order.save()
            messages.success(request, f"Payment successful! Your order #{order.id} is being processed.")
            return redirect('orders:success', pk=order.id)
        
        messages.error(request, "Payment verification failed.")
        return redirect('dashboard:home')

@csrf_exempt
def paystack_webhook(request):
    payload = request.body
    signature = request.headers.get('x-paystack-signature')
    
    if not PaystackService.verify_webhook(payload, signature):
        return HttpResponse(status=400)
    
    event_data = json.loads(payload)
    if event_data['event'] == 'charge.success':
        reference = event_data['data']['reference']
        order_id = event_data['data']['metadata']['order_id']
        order = Order.objects.filter(id=order_id).first()
        if order:
            order.payment_status = 'paid'
            order.paystack_ref = reference
            order.save()
            
    return HttpResponse(status=200)

class OrderSuccessView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'orders/order_success.html'
    context_object_name = 'order'
