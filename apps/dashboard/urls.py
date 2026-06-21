from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('bookings/', views.manage_booking_view, name='manage_bookings'),
]
