from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.tours.urls')),
    path('users/', include('apps.users.urls')),
    path('bookings/', include('apps.bookings.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
]


urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
