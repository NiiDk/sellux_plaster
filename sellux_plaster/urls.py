from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # 1. Admin must always be at the top with a trailing slash
    path('admin/', admin.site.urls),

    # 2. Authentication and Accounts
    path('accounts/', include('accounts.urls')),

    # 3. Main Business Apps
    path('', include('pages.urls')),
    path('services/', include('services.urls')),
    path('portfolio/', include('portfolio.urls')),
    path('catalogue/', include('catalogue.urls')),

    # 4. User Interaction & Requests
    path('faq/', include('faq.urls')),
    path('contact/', include('contact.urls')),
    path('orders/', include('orders.urls')),
    path('custom-requests/', include('custom_requests.urls')),

    # 5. Management & Content
    path('dashboard/', include('dashboard.urls')),
    path('insights/', include('blog.urls')),
]

# This handles Media (User Uploads) and Static files correctly
# In Production (Render), Whitenoise handles STATIC_URL,
# but Django still needs this helper for MEDIA_URL.
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # On Render, we still want to serve media files if not using S3/Cloudinary
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)