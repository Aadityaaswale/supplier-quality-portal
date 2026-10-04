from django.urls import path
from . import views

urlpatterns = [
    path('', views.supplier_list_view, name='supplier-list'),
    path('create/', views.supplier_create_view, name='supplier-create'),
    path('<int:pk>/', views.supplier_detail_view, name='supplier-detail'),
    path('<int:pk>/edit/', views.supplier_update_view, name='supplier-update'),
    path('<int:pk>/delete/', views.supplier_delete_view, name='supplier-delete'),
]
