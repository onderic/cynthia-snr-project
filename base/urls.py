from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('integrityportal.urls')),
    path('', include('accounts.urls')),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

# Add the following only if DEBUG is True in your settings.py
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
