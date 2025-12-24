from django.shortcuts import render
from django.views.generic import TemplateView
from django.db.models import Q
from catalogue.models import Product
from portfolio.models import Project
from services.models import Service
from blog.models import Post
from .models import Testimonial

class HomeView(TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch featured data for homepage
        context['featured_services'] = Service.objects.filter(is_active=True).order_by('order')[:3]
        context['latest_projects'] = Project.objects.all().order_by('-completion_date')[:3]
        context['testimonials'] = Testimonial.objects.filter(is_featured=True).order_by('-created_at')[:3]
        # Fetch latest blog posts
        context['latest_posts'] = Post.objects.filter(is_published=True).order_by('-created_at')[:3]
        return context

class AboutView(TemplateView):
    template_name = 'pages/about.html'

class TermsView(TemplateView):
    template_name = 'pages/terms.html'

class PrivacyView(TemplateView):
    template_name = 'pages/privacy.html'

class RefundView(TemplateView):
    template_name = 'pages/refund.html'

class ShippingView(TemplateView):
    template_name = 'pages/shipping.html'

def global_search(request):
    query = request.GET.get('q')
    product_results = []
    project_results = []
    
    if query:
        product_results = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
        project_results = Project.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
        
    return render(request, 'pages/search_results.html', {
        'query': query,
        'product_results': product_results,
        'project_results': project_results,
    })
