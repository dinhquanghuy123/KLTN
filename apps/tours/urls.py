from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('tour/<slug:slug>/', views.tour_detail_view, name='tour_detail'),
    path('tour/<int:pk>/review/', views.add_review_view, name='add_review'),
    path('wishlist/<int:tour_id>/', views.toggle_wishlist, name='toggle_wishlist'),
    path('my-wishlist/', views.my_wishlist, name='my_wishlist'),
]
