from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone', 'address')
    search_fields = ('user__username', 'phone')
    ordering = (
        'user__username',
    )

    list_per_page = 10
