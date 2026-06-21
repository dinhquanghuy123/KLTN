from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Sum, Count

from apps.tours.models import Tour
from apps.bookings.models import Booking
from django.contrib.admin.views.decorators import staff_member_required

from django.db.models.functions import TruncMonth
from django.core.exceptions import PermissionDenied


@staff_member_required
def dashboard_view(request):

    total_tours = Tour.objects.count()
    total_users = User.objects.count()
    total_bookings = Booking.objects.count()

    total_revenue = Booking.objects.aggregate(
        total=Sum('total_price')
    )['total'] or 0

    recent_bookings = Booking.objects.select_related(
        'user', 'tour'
    ).order_by('-booked_at')[:5]

    top_tours = Booking.objects.values(
        'tour__name'
    ).annotate(
        total=Sum('quantity')
    ).order_by('-total')[:5]

    booking_chart = Booking.objects.annotate(
        month=TruncMonth('booked_at')
    ).values('month').annotate(
        total=Count('id')
    ).order_by('month')

    context = {
        'total_tours': total_tours,
        'total_users': total_users,
        'total_bookings': total_bookings,
        'total_revenue': total_revenue,
        'recent_bookings': recent_bookings,
        'booking_chart': booking_chart,
        'top_tours': top_tours,
    }

    return render(request, 'dashboard/index.html', context)


@staff_member_required
def manage_booking_view(request):

    status = request.GET.get('status')

    bookings = Booking.objects.select_related(
        'user', 'tour').order_by('-booked_at')

    # filter theo status
    if status:
        bookings = bookings.filter(status=status)

    context = {
        'bookings': bookings
    }

    return render(request, 'dashboard/bookings.html', context)
