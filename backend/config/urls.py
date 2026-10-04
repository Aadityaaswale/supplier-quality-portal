"""
URL configuration for supplier_portal project.
Author: AADITYA ASWALE (23102B0044)
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.core.views import health_check_view

urlpatterns = [
    path('admin/', admin.site.urls),

    # Health Check (Public & automated monitor endpoint)
    path('health/', health_check_view, name='health-check'),

    # Modular App URLs
    path('', include('apps.dashboard.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('suppliers/', include('apps.suppliers.urls')),
    path('reviews/', include('apps.reviews.urls')),
    path('reports/', include('apps.reports.urls')),

    # REST API endpoints
    path('api/', include([
        path('suppliers/', include('apps.suppliers.api_urls')),
        path('reviews/', include('apps.reviews.api_urls')),
        path('dashboard/', include('apps.dashboard.api_urls')),
    ])),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'apps.core.views.custom_404_view'
handler500 = 'apps.core.views.custom_500_view'
handler403 = 'apps.core.views.custom_403_view'
