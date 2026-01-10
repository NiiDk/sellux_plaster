from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

# Custom Branding for Django Administration
admin.site.site_header = "Sellux Plaster Administration"
admin.site.site_title = "Sellux Plaster Admin Portal"
admin.site.index_title = "Welcome to Sellux Plaster Business Manager"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('pages.urls')),
    path('services/', include('services.urls')),
    path('portfolio/', include('portfolio.urls')),
    path('shop/', include('catalogue.urls')), # Renamed from 'catalogue'
    path('faq/', include('faq.urls')),
    path('contact/', include('contact.urls')),
    path('orders/', include('orders.urls')),
    path('custom-requests/', include('custom_requests.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('insights/', include('blog.urls')),
    path('cart/', include('cart.urls')),
    path('estimation/', include('estimation.urls')),
    path('promotions/', include('promotions.urls')),
    path('about/', include('about.urls')),
    path('team/', include('team.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
