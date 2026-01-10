from django.shortcuts import render
from .models import AboutPage

def about_view(request):
    about_page = AboutPage.objects.first()
    return render(request, 'about/about.html', {'about_page': about_page})
