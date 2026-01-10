from django.urls import path
from . import views

app_name = 'team'

urlpatterns = [
    path('', views.team_list_view, name='team_list'),
    path('<int:pk>/', views.team_detail_view, name='team_detail'),
]
