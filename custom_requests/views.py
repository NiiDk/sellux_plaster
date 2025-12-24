from django.views.generic import CreateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import CustomRequest
from .forms import CustomRequestForm

class CustomRequestCreateView(LoginRequiredMixin, CreateView):
    model = CustomRequest
    form_class = CustomRequestForm
    template_name = 'custom_requests/request_form.html'
    success_url = reverse_lazy('custom_requests:request_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class CustomRequestListView(LoginRequiredMixin, ListView):
    model = CustomRequest
    template_name = 'custom_requests/request_list.html'
    context_object_name = 'requests'

    def get_queryset(self):
        return CustomRequest.objects.filter(user=self.request.user).order_by('-created_at')
