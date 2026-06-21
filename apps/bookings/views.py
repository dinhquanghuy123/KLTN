from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from apps.tours.models import Tour
from .models import Booking, Coupon
from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction

from django.conf import settings
from datetime import datetime
from apps.payments.vnpay import VNPay


@login_required
@transaction.atomic
def create_booking_view(request, pk):
    tour = get_object_or_404(Tour, pk=pk)

    if request.method == 'POST':

        try:
            quantity = int(request.POST.get('quantity', 1))
        except ValueError:
            messages.error(request, 'Số lượng không hợp lệ.')
            return redirect('create_booking', pk=tour.id)

        # Validate
        if quantity <= 0:
            messages.error(request, 'Số lượng không hợp lệ.')
            return redirect('create_booking', pk=tour.id)

        if quantity > tour.slots:
            messages.error(request, 'Không đủ chỗ trống.')
            return redirect('create_booking', pk=tour.id)

        coupon_code = request.POST.get(
            'coupon'
        )

        # Tạo booking
        coupon = None
        discount_amount = 0

        if coupon_code:

            coupon = Coupon.objects.filter(
                code__iexact=coupon_code,
                active=True
            ).first()

        if coupon_code and not coupon:
            messages.warning(
                request,
                'Mã giảm giá không hợp lệ'
            )

        if coupon:

            total = tour.price * quantity

            discount_amount = (
                total * coupon.discount
            ) / 100

        booking = Booking.objects.create(

            user=request.user,
            tour=tour,
            quantity=quantity,

            coupon=coupon,
            discount_amount=discount_amount
        )

        # Trừ slot
        tour.slots -= quantity
        tour.save()

        messages.success(request, 'Đặt tour thành công!')

        return redirect('booking_history')

    return render(request, 'bookings/create.html', {
        'tour': tour
    })


@login_required
def booking_history_view(request):

    bookings = Booking.objects.filter(
        user=request.user
    ).select_related('tour')

    return render(request, 'bookings/history.html', {
        'bookings': bookings
    })


@login_required
@transaction.atomic
def cancel_booking_view(request, pk):
    booking = get_object_or_404(
        Booking.objects.select_related('tour').select_for_update(),
        pk=pk,
        user=request.user
    )

    # ❗ chỉ cho hủy khi chưa hủy
    if booking.status == 'cancelled':
        messages.warning(request, "Booking đã bị hủy trước đó")
        return redirect('booking_history')

    if booking.status != 'pending':
        messages.error(request, "Không thể hủy booking này")
        return redirect('booking_history')

    # ✅ hoàn lại slot
    tour = booking.tour
    tour.slots += booking.quantity
    tour.save()

    # ✅ cập nhật trạng thái
    booking.status = 'cancelled'
    booking.save()

    messages.success(request, "Hủy booking thành công")

    return redirect('booking_history')


@staff_member_required
def confirm_booking_view(request, pk):
    booking = get_object_or_404(Booking, pk=pk)

    if booking.status != 'pending':
        messages.warning(request, "Booking này không thể xác nhận")
        return redirect('dashboard')  # hoặc trang admin riêng

    booking.status = 'confirmed'
    booking.save()

    messages.success(request, "Xác nhận booking thành công")

    return redirect('dashboard')


@login_required
def create_payment(request, booking_id):

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user
    )

    # chặn thanh toán lại
    if booking.payment_status == 'paid':
        messages.warning(
            request,
            'Booking đã thanh toán'
        )
        return redirect('booking_history')

    vnp = VNPay()

    vnp.request_data = {
        'vnp_Version': '2.1.0',
        'vnp_Command': 'pay',
        'vnp_TmnCode': settings.VNPAY_TMN_CODE,
        'vnp_Amount': int(booking.tour.price) * 100,
        'vnp_CurrCode': 'VND',
        'vnp_TxnRef': str(booking.id),
        'vnp_OrderInfo': f'Payment for booking {booking.id}',
        'vnp_OrderType': 'other',
        'vnp_Locale': 'vn',
        'vnp_ReturnUrl': settings.VNPAY_RETURN_URL,
        'vnp_IpAddr': request.META.get(
            'REMOTE_ADDR',
            '127.0.0.1'
        ),
        'vnp_CreateDate': datetime.now().strftime('%Y%m%d%H%M%S'),
    }

    payment_url = vnp.get_payment_url(
        settings.VNPAY_PAYMENT_URL,
        settings.VNPAY_HASH_SECRET
    )
    print(vnp.request_data)
    print(payment_url)
    return redirect(payment_url)


@login_required
def payment_return(request):

    response_code = request.GET.get('vnp_ResponseCode')

    booking_id = request.GET.get('vnp_TxnRef')

    booking = get_object_or_404(
        Booking,
        id=booking_id
    )

    # THANH TOÁN THÀNH CÔNG
    if response_code == '00':

        booking.payment_status = 'paid'
        booking.status = 'confirmed'

        booking.save()

    # THANH TOÁN THẤT BẠI
    else:

        booking.payment_status = 'failed'

        booking.save()

    return render(
        request,
        'bookings/payment_result.html',
        {
            'booking': booking
        }
    )
