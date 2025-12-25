import json
import logging
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
from core.services import PaystackService, NotificationService

logger = logging.getLogger(__name__)

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

        order = Order.objects.create(
            user=request.user,
            first_name=request.user.first_name or request.user.username,
            last_name=request.user.last_name or "Client",
            email=request.user.email,
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            total_amount=cart.get_total_price()
        )
        
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity']
            )
        
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
            
            # Defensive check: if already paid via webhook, just show success
            if order.payment_status != 'paid':
                order.payment_status = 'paid'
                order.payment_channel = data.get('channel', 'unknown')
                order.transaction_id = data.get('id')
                order.save()
                
            messages.success(request, f"Payment successful! Your order #{order.id} is being processed.")
            return redirect('orders:success', pk=order.id)
        
        messages.error(request, "Payment verification failed or timed out.")
        return redirect('dashboard:home')

@csrf_exempt
def paystack_webhook(request):
    """
    Production-grade Webhook Guard for Sellux Plaster.
    Handles background verification and state persistence.
    """
    payload = request.body
    signature = request.headers.get('x-paystack-signature')
    
    if not PaystackService.verify_webhook(payload, signature):
        logger.warning(f"Invalid Paystack Webhook Signature received.")
        return HttpResponse(status=400)
    
    try:
        event_data = json.loads(payload)
        event_type = event_data.get('event')
        
        if event_type == 'charge.success':
            data = event_data['data']
            reference = data['reference']
            order_id = data['metadata'].get('order_id')
            
            order = Order.objects.filter(id=order_id).first()
            if order and order.payment_status != 'paid':
                order.payment_status = 'paid'
                order.paystack_ref = reference
                order.payment_channel = data.get('channel', 'webhook')
                order.transaction_id = data.get('id')
                order.save()
                
                # Automated artisan touch: Notify the sales team via internal log
                logger.info(f"ORDER PAID (WEBHOOK): Order #{order.id} verified via Paystack.")
                
        return HttpResponse(status=200)
        
    except (json.JSONDecodeError, KeyError) as e:
        logger.error(f"Webhook processing error: {str(e)}")
        return HttpResponse(status=400)

class OrderSuccessView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'orders/order_success.html'
    context_object_name = 'order'
