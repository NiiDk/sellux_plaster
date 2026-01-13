from django.shortcuts import render
from .models import AboutPage

def about_view(request):
    # 1. Fetch the data from the database
    about_page = AboutPage.objects.last()
    
    # 2. Package it into a "context" dictionary
    context = {
        'about_page': about_page,
    }
    
    # 3. Send that context to the template
    return render(request, 'about/about.html', context)