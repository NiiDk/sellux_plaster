from django.views.generic import ListView, DetailView
from .models import Project

class PortfolioListView(ListView):
    """Displays a paginated list of portfolio projects."""
    model = Project
    template_name = 'portfolio/portfolio_list.html'
    context_object_name = 'projects'
    paginate_by = 12

class PortfolioDetailView(DetailView):
    """Shows a single portfolio project."""
    model = Project
    template_name = 'portfolio/portfolio_detail.html'
    context_object_name = 'project'
