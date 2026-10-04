from django.urls import path
from . import views

urlpatterns = [
    path('', views.reports_view, name='reports-index'),
    path('export/suppliers/', views.export_suppliers_csv, name='export-suppliers-csv'),
    path('export/reviews/', views.export_reviews_csv, name='export-reviews-csv'),
]
