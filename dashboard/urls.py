from django.urls import path
from .views import (
    UserDashboardView, AdminDashboardView, AdminBIView, 
    ProductListView, ProductCreateView, ProductUpdateView, ProductDeleteView,
    OrderListView, OrderDetailView, OrderUpdateView,
    UserListView, UserDetailView, UserUpdateView,
    EstimationServiceListView, EstimationServiceCreateView, EstimationServiceUpdateView, EstimationServiceDeleteView,
    BlogPostListView, BlogPostCreateView, BlogPostUpdateView, BlogPostDeleteView,
    PromotionListView, PromotionCreateView, PromotionUpdateView, PromotionDeleteView
)

app_name = 'dashboard'

urlpatterns = [
    path('', UserDashboardView.as_view(), name='home'),
    path('admin/', AdminDashboardView.as_view(), name='admin_home'),
    path('admin/intel/', AdminBIView.as_view(), name='admin_intel'),

    path('admin/products/', ProductListView.as_view(), name='product_list'),
    path('admin/products/create/', ProductCreateView.as_view(), name='product_create'),
    path('admin/products/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('admin/products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),

    path('admin/orders/', OrderListView.as_view(), name='order_list'),
    path('admin/orders/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('admin/orders/<int:pk>/update/', OrderUpdateView.as_view(), name='order_update'),

    path('admin/users/', UserListView.as_view(), name='user_list'),
    path('admin/users/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('admin/users/<int:pk>/update/', UserUpdateView.as_view(), name='user_update'),

    path('admin/services/', EstimationServiceListView.as_view(), name='service_list'),
    path('admin/services/create/', EstimationServiceCreateView.as_view(), name='service_create'),
    path('admin/services/<int:pk>/update/', EstimationServiceUpdateView.as_view(), name='service_update'),
    path('admin/services/<int:pk>/delete/', EstimationServiceDeleteView.as_view(), name='service_delete'),

    path('admin/blog/', BlogPostListView.as_view(), name='blog_post_list'),
    path('admin/blog/create/', BlogPostCreateView.as_view(), name='blog_post_create'),
    path('admin/blog/<int:pk>/update/', BlogPostUpdateView.as_view(), name='blog_post_update'),
    path('admin/blog/<int:pk>/delete/', BlogPostDeleteView.as_view(), name='blog_post_delete'),

    path('admin/promotions/', PromotionListView.as_view(), name='promotion_list'),
    path('admin/promotions/create/', PromotionCreateView.as_view(), name='promotion_create'),
    path('admin/promotions/<int:pk>/update/', PromotionUpdateView.as_view(), name='promotion_update'),
    path('admin/promotions/<int:pk>/delete/', PromotionDeleteView.as_view(), name='promotion_delete'),
]
