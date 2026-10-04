from django.urls import path
from . import views

urlpatterns = [
    path('', views.review_list_view, name='review-list'),
    path('create/', views.review_create_view, name='review-create'),
    path('<int:pk>/', views.review_detail_view, name='review-detail'),
    path('<int:pk>/edit/', views.review_update_view, name='review-update'),
    path('<int:pk>/transition/', views.review_transition_view, name='review-transition'),
]
