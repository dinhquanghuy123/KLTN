from django.db import models
from django.contrib.auth.models import User
from apps.tours.models import Tour

import qrcode
from io import BytesIO
from django.core.files import File


class Coupon(models.Model):

    code = models.CharField(
        max_length=20,
        unique=True
    )

    discount = models.PositiveIntegerField(
        help_text="Phần trăm giảm"
    )

    active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.code} ({self.discount}%)"


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Chờ xác nhận'),
        ('confirmed', 'Đã xác nhận'),
        ('cancelled', 'Đã hủy'),
        ('completed', 'Hoàn thành'),
    ]

    PAYMENT_STATUS = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField(default=1)

    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    coupon = models.ForeignKey(
        Coupon,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    discount_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default='pending'
    )

    booked_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    qr_code = models.ImageField(
        upload_to='booking_qr/',
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['-booked_at']

    def __str__(self):
        return f"{self.user.username} - {self.tour.name}"

    def save(self, *args, **kwargs):
        total = self.quantity * self.tour.price

        self.total_price = (
            total - self.discount_amount
        )
        super().save(*args, **kwargs)

        if not self.qr_code:

            qr = qrcode.make(
                f"Booking ID: {self.id}"
            )

            buffer = BytesIO()

            qr.save(buffer)

            self.qr_code.save(
                f'booking-{self.id}.png',
                File(buffer),
                save=False
            )

            super().save(
                update_fields=['qr_code']
            )
