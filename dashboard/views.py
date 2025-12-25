from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Sum, Count, Q
from decimal import Decimal

from orders.models import Order
from custom_requests.models import CustomRequest
from catalogue.models import Product

class UserDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/user_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_orders = Order.objects.filter(user=self.request.user).order_by('-created_at')
        context['orders'] = user_orders
        context['total_spent'] = user_orders.filter(payment_status='paid').aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        context['custom_requests'] = CustomRequest.objects.filter(user=self.request.user).order_by('-created_at')
        return context

class AdminBIView(UserPassesTestMixin, TemplateView):
    """
    Business Intelligence Dashboard for Sellux Plaster Admins.
    """
    template_name = 'dashboard/admin_bi.html'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 1. Financial Overview
        paid_orders = Order.objects.filter(payment_status='paid')
        context['gross_revenue'] = paid_orders.aggregate(Sum('total_amount'))['total_amount__sum'] or Decimal('0.00')
        context['pending_revenue'] = Order.objects.filter(payment_status='pending').aggregate(Sum('total_amount'))['total_amount__sum'] or Decimal('0.00')
        
        # 2. Conversion Analytics (The "Success" Funnel)
        total_requests = CustomRequest.objects.count()
        accepted_requests = CustomRequest.objects.filter(status='accepted').count()
        paid_requests = CustomRequest.objects.filter(status='paid').count()
        
        context['request_stats'] = {
            'total': total_requests,
            'accepted': accepted_requests,
            'paid': paid_requests,
            'conversion_rate': round((paid_requests / total_requests * 100), 1) if total_requests > 0 else 0
        }

        # 3. Product Performance
        context['top_products'] = Product.objects.annotate(
            sales_count=Count('order_items', filter=Q(order_items__order__payment_status='paid'))
        ).order_by('-sales_count')[:5]

        # 4. Recent Activity Feed
        context['recent_orders'] = Order.objects.all().order_by('-created_at')[:10]
        
        return context
