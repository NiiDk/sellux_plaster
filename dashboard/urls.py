from django.urls import path
from .views import UserDashboardView, AdminDashboardView

app_name = 'dashboard'

urlpatterns = [
    path('', UserDashboardView.as_view(), name='home'), # Changed from 'user' to 'home' to match templates
    path('admin/', AdminDashboardView.as_view(), name='admin'),
]
