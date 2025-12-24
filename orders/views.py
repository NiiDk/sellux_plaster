import requests
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, TemplateView
from catalogue.models import Product
from .models import Order

class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    template_name = 'orders/order_form.html'
    fields = [] # Handled manually via GET params for now

    def get(self, request, *args, **kwargs):
        product_id = request.GET.get('product')
        quantity = int(request.GET.get('quantity', 1))
        product = get_object_or_404(Product, id=product_id)
        
        # 1. Create the Local Order
        total_amount = product.price * quantity
        order = Order.objects.create(
            user=request.user,
            product=product,
            quantity=quantity,
            total_amount=total_amount,
            payment_status='pending'
        )

        # 2. Initialize Paystack Transaction
        url = "https://api.paystack.co/transaction/initialize"
        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }
        data = {
            "email": request.user.email,
            "amount": int(total_amount * 100), # Paystack expects amount in pesewas
            "currency": "GHS",
            "callback_url": request.build_absolute_uri(reverse('orders:success', args=[order.id])),
            "metadata": {"order_id": order.id}
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            res_data = response.json()
            if res_data['status']:
                # Redirect user to Paystack Checkout Page
                return redirect(res_data['data']['authorization_url'])
            else:
                return redirect('catalogue:product_list')
        except Exception:
            return redirect('catalogue:product_list')

class OrderSuccessView(LoginRequiredMixin, TemplateView):
    template_name = 'orders/order_success.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        order = get_object_or_404(Order, id=self.kwargs.get('pk'), user=self.request.user)
        # In a real app, you would verify the payment here via Paystack API
        order.payment_status = 'paid'
        order.save()
        ctx['order'] = order
        return ctx
