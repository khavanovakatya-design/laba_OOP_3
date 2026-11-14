from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import os

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls'))
]

if settings.DEBUG:
    urlpatterns += static('/assets/', document_root=os.path.join(settings.BASE_DIR, 'assets'))
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)