from django.urls import path
from . import views

urlpatterns = [
    path('create/<int:pk>/', views.create_booking_view, name='create_booking'),
    path('history/', views.booking_history_view, name='booking_history'),
    path('cancel/<int:pk>/',
         views.cancel_booking_view, name='cancel_booking'),
    path('confirm/<int:pk>/',
         views.confirm_booking_view, name='confirm_booking'),
    path('payment/<int:booking_id>/',
         views.create_payment, name='create_payment'),
    path('payment-return/',
         views.payment_return, name='payment_return'),
]
