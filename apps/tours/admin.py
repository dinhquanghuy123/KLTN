from django.contrib import admin
from .models import Tour, Review


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'destination',
                    'price', 'slots', 'created_at', 'featured')
    search_fields = ('name', 'destination')
    list_filter = ('destination',)
    list_editable = ('price', 'slots', 'featured')
    ordering = ('-created_at',)
    list_per_page = 10


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'tour', 'rating', 'created_at')
    search_fields = ('user__username', 'tour__name')
    list_filter = ('rating',)
    ordering = ('-created_at',)
    list_per_page = 10
