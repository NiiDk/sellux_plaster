from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView
from orders.models import Order


class UserDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/user_dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['orders'] = Order.objects.filter(user=self.request.user).order_by('-created_at')[:10]
        return ctx


class AdminDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'dashboard/admin_dashboard.html'

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['recent_orders'] = Order.objects.all().order_by('-created_at')[:20]
        ctx['user_count'] = self.request.user.__class__.objects.count()
        return ctx
