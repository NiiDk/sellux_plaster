from django.urls import path
from .views import PortfolioListView, PortfolioDetailView

app_name = 'portfolio'

urlpatterns = [
    path('', PortfolioListView.as_view(), name='project_list'),
    path('<slug:slug>/', PortfolioDetailView.as_view(), name='project_detail'),
]
