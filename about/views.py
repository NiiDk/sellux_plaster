from django.shortcuts import render
from .models import AboutPage

def about_view(request):
    # Get the first AboutPage object, or None if it doesn't exist
    about_page = AboutPage.objects.first()
    
    context = {
        'about_page': about_page,
    }
    return render(request, 'about/about.html', context)