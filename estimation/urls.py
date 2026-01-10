from django.urls import path
from . import views

app_name = 'estimation'

urlpatterns = [
    path('', views.estimation_view, name='estimator'),
]
