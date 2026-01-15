from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse
from .sitemaps import StaticViewSitemap

# Custom Branding
admin.site.site_header = "Sellux Plaster Administration"
admin.site.site_title = "Sellux Plaster Admin Portal"
admin.site.index_title = "Welcome to Sellux Plaster Business Manager"

sitemaps = {
    'static': StaticViewSitemap,
}

def robots_txt(request):
    content = (
        "User-agent: *\n"
        "Disallow: /admin/\n"
        "Disallow: /dashboard/\n\n"
        "Sitemap: https://selluxplaster.com/sitemap.xml"
    )
    return HttpResponse(content, content_type="text/plain")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('services/', include('services.urls')),
    path('portfolio/', include('portfolio.urls')),
    path('shop/', include('catalogue.urls')), 
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
    path('', include('pages.urls')),
    path('robots.txt', robots_txt),
    # Sitemap and Robots.txt (Corrected Integration)
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)