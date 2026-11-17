from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
import os

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('', include('users.urls')),
    path('login/', RedirectView.as_view(url='/login')),
    path('register/', RedirectView.as_view(url='/register')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=os.path.join(settings.BASE_DIR, 'assets'))
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static('/assets/', document_root=os.path.join(settings.BASE_DIR, 'assets'))