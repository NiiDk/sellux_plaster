from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages

from .models import CustomRequest
from .forms import CustomRequestForm
from orders.models import Order

class CustomRequestCreateView(LoginRequiredMixin, CreateView):
    model = CustomRequest
    form_class = CustomRequestForm
    template_name = 'custom_requests/request_form.html'
    success_url = reverse_lazy('custom_requests:request_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Your bespoke design request has been submitted. Our architects will review it and provide a quote soon.")
        return super().form_valid(form)

class CustomRequestListView(LoginRequiredMixin, ListView):
    model = CustomRequest
    template_name = 'custom_requests/request_list.html'
    context_object_name = 'requests'

    def get_queryset(self):
        return CustomRequest.objects.filter(user=self.request.user).order_by('-created_at')

class CustomRequestDetailView(LoginRequiredMixin, DetailView):
    model = CustomRequest
    template_name = 'custom_requests/request_detail.html'
    context_object_name = 'req'

def accept_quote(request, pk):
    """
    View to convert an accepted quote into a payable order.
    """
    custom_request = get_object_or_404(CustomRequest, pk=pk, user=request.user, status='quoted')
    
    # 1. Create a shadow Order for this custom project
    order = Order.objects.create(
        user=request.user,
        first_name=request.user.first_name or request.user.username,
        last_name=request.user.last_name,
        email=request.user.email,
        total_amount=custom_request.quoted_price,
        address="Site Visit Required", # Placeholder for manual follow-up
        city="Accra"
    )
    
    # 2. Link them
    custom_request.status = 'accepted'
    custom_request.order = order
    custom_request.save()
    
    messages.success(request, "Quote accepted! You can now proceed to payment.")
    return redirect('dashboard:home')
