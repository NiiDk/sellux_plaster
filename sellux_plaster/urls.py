from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin must have a trailing slash
    path('admin/', admin.site.urls),

    path('accounts/', include('accounts.urls')),
    path('', include('pages.urls')),
    path('services/', include('services.urls')),
    path('portfolio/', include('portfolio.urls')),
    path('catalogue/', include('catalogue.urls')),
    path('faq/', include('faq.urls')),
    path('contact/', include('contact.urls')),
    path('orders/', include('orders.urls')),
    path('custom-requests/', include('custom_requests.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('insights/', include('blog.urls')),
]

# Standard static/media serving for development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
