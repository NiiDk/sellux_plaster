import json
import logging
from decimal import Decimal
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib import messages
from django.template.loader import get_template
from xhtml2pdf import pisa

from .models import Order, OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from core.services import PaystackService, NotificationService
from shipping.models import City, ShippingSetting

logger = logging.getLogger(__name__)

class OrderCreateView(View):
    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        if len(cart) == 0:
            messages.warning(request, "Your cart is empty. Please add items before checking out.")
            return redirect('catalogue:product_list')

        form = OrderCreateForm(user=request.user if request.user.is_authenticated else None)
        shipping_settings = ShippingSetting.objects.first()
        tax_rate = shipping_settings.tax_rate if shipping_settings else 0
        
        context = {
            'cart': cart,
            'form': form,
            'tax_rate': tax_rate,
        }
        return render(request, 'orders/order_create.html', context)

    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        form = OrderCreateForm(request.POST, user=request.user if request.user.is_authenticated else None)

        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            
            subtotal = cart.get_total_price()
            shipping_settings = ShippingSetting.objects.first()
            tax_rate = Decimal(shipping_settings.tax_rate if shipping_settings else 0)
            order.tax = subtotal * (tax_rate / Decimal(100))

            if order.delivery_option == 'delivery':
                city_name = form.cleaned_data['city']
                city = City.objects.get(name=city_name)
                base_fee = Decimal(city.base_delivery_fee)
                variable_fee = (subtotal / 100) * (Decimal(shipping_settings.delivery_fee_per_100) if shipping_settings else 0)
                order.delivery_fee = base_fee + variable_fee
            
            order.total_amount = subtotal
            order.save()

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
                amount_in_cedis=order.get_grand_total(),
                callback_url=callback_url,
                metadata={'order_id': order.id}
            )

            if res and res['status']:
                order.paystack_ref = res['data']['reference']
                order.save()
                cart.clear()
                return redirect(res['data']['authorization_url'])

            messages.error(request, 'Payment initialization failed. Please try again.')
            return render(request, 'orders/order_create.html', {'cart': cart, 'form': form})

        return render(request, 'orders/order_create.html', {'cart': cart, 'form': form})

class OrderVerifyView(View):
    def get(self, request, *args, **kwargs):
        reference = request.GET.get('reference')
        success, data = PaystackService.verify_payment(reference)

        if success:
            order_id = data['metadata']['order_id']
            order = get_object_or_404(Order, id=order_id)

            if order.payment_status != 'paid':
                order.payment_status = 'paid'
                order.payment_channel = data.get('channel', 'unknown')
                order.transaction_id = data.get('id')
                order.save()

                # Send order confirmation email
                NotificationService.send_email(
                    subject=f"Your Sellux Plaster Order #{order.id} is Confirmed!",
                    recipient_list=[order.email],
                    template_name='emails/order_confirmation.html',
                    context={'order': order, 'request': request}
                )

            messages.success(request, f"Payment successful! Your order #{order.id} is being processed.")
            return redirect('orders:success', pk=order.id)

        messages.error(request, "Payment verification failed or timed out. Please try again.")
        return redirect('catalogue:product_list')

@csrf_exempt
def paystack_webhook(request):
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

                logger.info(f"ORDER PAID (WEBHOOK): Order #{order.id} verified via Paystack.")

        return HttpResponse(status=200)

    except (json.JSONDecodeError, KeyError) as e:
        logger.error(f"Webhook processing error: {str(e)}")
        return HttpResponse(status=400)

class OrderSuccessView(DetailView):
    model = Order
    template_name = 'orders/order_success.html'
    context_object_name = 'order'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Order.objects.filter(user=self.request.user, pk=self.kwargs['pk'])
        return Order.objects.filter(pk=self.kwargs['pk'])

def download_invoice_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    template_path = 'orders/invoice_pdf.html'
    context = {'order': order}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_#{order.id}.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
