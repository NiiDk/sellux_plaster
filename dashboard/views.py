from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from django.db.models import Sum, Count, Q
from django.urls import reverse_lazy
from decimal import Decimal

from orders.models import Order
from custom_requests.models import CustomRequest
from catalogue.models import Product
from estimation.models import Service as EstimationService
from blog.models import Post as BlogPost
from promotions.models import Promotion

User = get_user_model()

class UserDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/user_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_orders = Order.objects.filter(user=self.request.user).order_by('-created_at')
        context['orders'] = user_orders
        context['total_spent'] = user_orders.filter(payment_status='paid').aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        context['custom_requests'] = CustomRequest.objects.filter(user=self.request.user).order_by('-created_at')
        return context

class AdminDashboardView(UserPassesTestMixin, TemplateView):
    template_name = 'dashboard/admin_dashboard.html'

    def test_func(self):
        return self.request.user.is_staff

class AdminBIView(UserPassesTestMixin, TemplateView):
    template_name = 'dashboard/admin_bi.html'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paid_orders = Order.objects.filter(payment_status='paid')
        context['gross_revenue'] = paid_orders.aggregate(Sum('total_amount'))['total_amount__sum'] or Decimal('0.00')
        context['pending_revenue'] = Order.objects.filter(payment_status='pending').aggregate(Sum('total_amount'))['total_amount__sum'] or Decimal('0.00')
        total_requests = CustomRequest.objects.count()
        accepted_requests = CustomRequest.objects.filter(status='accepted').count()
        paid_requests = CustomRequest.objects.filter(status='paid').count()
        context['request_stats'] = {
            'total': total_requests,
            'accepted': accepted_requests,
            'paid': paid_requests,
            'conversion_rate': round((paid_requests / total_requests * 100), 1) if total_requests > 0 else 0
        }
        context['top_products'] = Product.objects.annotate(
            sales_count=Count('order_items', filter=Q(order_items__order__payment_status='paid'))
        ).order_by('-sales_count')[:5]
        context['recent_orders'] = Order.objects.all().order_by('-created_at')[:10]
        return context

class ProductListView(UserPassesTestMixin, ListView):
    model = Product
    template_name = 'dashboard/product_list.html'
    context_object_name = 'products'
    def test_func(self):
        return self.request.user.is_staff

class ProductCreateView(UserPassesTestMixin, CreateView):
    model = Product
    template_name = 'dashboard/product_form.html'
    fields = '__all__'
    success_url = reverse_lazy('dashboard:product_list')
    def test_func(self):
        return self.request.user.is_staff

class ProductUpdateView(UserPassesTestMixin, UpdateView):
    model = Product
    template_name = 'dashboard/product_form.html'
    fields = '__all__'
    success_url = reverse_lazy('dashboard:product_list')
    def test_func(self):
        return self.request.user.is_staff

class ProductDeleteView(UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'dashboard/product_confirm_delete.html'
    success_url = reverse_lazy('dashboard:product_list')
    def test_func(self):
        return self.request.user.is_staff

class OrderListView(UserPassesTestMixin, ListView):
    model = Order
    template_name = 'dashboard/order_list.html'
    context_object_name = 'orders'
    paginate_by = 20
    ordering = ['-created_at']
    def test_func(self):
        return self.request.user.is_staff

class OrderDetailView(UserPassesTestMixin, DetailView):
    model = Order
    template_name = 'dashboard/order_detail.html'
    context_object_name = 'order'
    def test_func(self):
        return self.request.user.is_staff

class OrderUpdateView(UserPassesTestMixin, UpdateView):
    model = Order
    template_name = 'dashboard/order_form.html'
    fields = ['status', 'payment_status', 'admin_feedback']
    def get_success_url(self):
        return reverse_lazy('dashboard:order_detail', kwargs={'pk': self.object.pk})
    def test_func(self):
        return self.request.user.is_staff

class UserListView(UserPassesTestMixin, ListView):
    model = User
    template_name = 'dashboard/user_list.html'
    context_object_name = 'users'
    def test_func(self):
        return self.request.user.is_staff

class UserDetailView(UserPassesTestMixin, DetailView):
    model = User
    template_name = 'dashboard/user_detail.html'
    context_object_name = 'user_obj'
    def test_func(self):
        return self.request.user.is_staff

class UserUpdateView(UserPassesTestMixin, UpdateView):
    model = User
    template_name = 'dashboard/user_form.html'
    fields = ['first_name', 'last_name', 'email', 'is_staff']
    def get_success_url(self):
        return reverse_lazy('dashboard:user_detail', kwargs={'pk': self.object.pk})
    def test_func(self):
        return self.request.user.is_staff

class EstimationServiceListView(UserPassesTestMixin, ListView):
    model = EstimationService
    template_name = 'dashboard/service_list.html'
    context_object_name = 'services'
    def test_func(self):
        return self.request.user.is_staff

class EstimationServiceCreateView(UserPassesTestMixin, CreateView):
    model = EstimationService
    template_name = 'dashboard/service_form.html'
    fields = ['name', 'cost_per_sqm', 'is_active']
    success_url = reverse_lazy('dashboard:service_list')
    def test_func(self):
        return self.request.user.is_staff

class EstimationServiceUpdateView(UserPassesTestMixin, UpdateView):
    model = EstimationService
    template_name = 'dashboard/service_form.html'
    fields = ['name', 'cost_per_sqm', 'is_active']
    success_url = reverse_lazy('dashboard:service_list')
    def test_func(self):
        return self.request.user.is_staff

class EstimationServiceDeleteView(UserPassesTestMixin, DeleteView):
    model = EstimationService
    template_name = 'dashboard/service_confirm_delete.html'
    success_url = reverse_lazy('dashboard:service_list')
    def test_func(self):
        return self.request.user.is_staff

class BlogPostListView(UserPassesTestMixin, ListView):
    model = BlogPost
    template_name = 'dashboard/blog_post_list.html'
    context_object_name = 'posts'
    def test_func(self):
        return self.request.user.is_staff

class BlogPostCreateView(UserPassesTestMixin, CreateView):
    model = BlogPost
    template_name = 'dashboard/blog_post_form.html'
    fields = ['title', 'slug', 'author', 'category', 'featured_image', 'excerpt', 'content', 'is_published']
    success_url = reverse_lazy('dashboard:blog_post_list')
    def test_func(self):
        return self.request.user.is_staff

class BlogPostUpdateView(UserPassesTestMixin, UpdateView):
    model = BlogPost
    template_name = 'dashboard/blog_post_form.html'
    fields = ['title', 'slug', 'author', 'category', 'featured_image', 'excerpt', 'content', 'is_published']
    success_url = reverse_lazy('dashboard:blog_post_list')
    def test_func(self):
        return self.request.user.is_staff

class BlogPostDeleteView(UserPassesTestMixin, DeleteView):
    model = BlogPost
    template_name = 'dashboard/blog_post_confirm_delete.html'
    success_url = reverse_lazy('dashboard:blog_post_list')
    def test_func(self):
        return self.request.user.is_staff

class PromotionListView(UserPassesTestMixin, ListView):
    model = Promotion
    template_name = 'dashboard/promotion_list.html'
    context_object_name = 'promotions'
    def test_func(self):
        return self.request.user.is_staff

class PromotionCreateView(UserPassesTestMixin, CreateView):
    model = Promotion
    template_name = 'dashboard/promotion_form.html'
    fields = ['title', 'description', 'image', 'is_active']
    success_url = reverse_lazy('dashboard:promotion_list')
    def test_func(self):
        return self.request.user.is_staff

class PromotionUpdateView(UserPassesTestMixin, UpdateView):
    model = Promotion
    template_name = 'dashboard/promotion_form.html'
    fields = ['title', 'description', 'image', 'is_active']
    success_url = reverse_lazy('dashboard:promotion_list')
    def test_func(self):
        return self.request.user.is_staff

class PromotionDeleteView(UserPassesTestMixin, DeleteView):
    model = Promotion
    template_name = 'dashboard/promotion_confirm_delete.html'
    success_url = reverse_lazy('dashboard:promotion_list')
    def test_func(self):
        return self.request.user.is_staff
