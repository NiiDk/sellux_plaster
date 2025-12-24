from django.urls import path
from .views import CustomRequestCreateView, CustomRequestListView

app_name = 'custom_requests'

urlpatterns = [
    path('new/', CustomRequestCreateView.as_view(), name='request_create'),
    path('my-requests/', CustomRequestListView.as_view(), name='request_list'),
]
