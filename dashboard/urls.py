from django.urls import path
from .views import UserDashboardView, AdminBIView

app_name = 'dashboard'

urlpatterns = [
    path('', UserDashboardView.as_view(), name='home'),
    path('intel/', AdminBIView.as_view(), name='admin_intel'),
]
