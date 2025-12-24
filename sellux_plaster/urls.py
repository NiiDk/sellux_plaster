from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('pages.urls')),
    path('faq/', include('faq.urls')),
    path('contact/', include('contact.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('portfolio/', include('portfolio.urls')),
    path('catalogue/', include('catalogue.urls')),
    path('orders/', include('orders.urls')),
    path('custom-requests/', include('custom_requests.urls')),
    path('services/', include('services.urls')),
    path('insights/', include('blog.urls')),
]

# Serve media files locally during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
