from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import os
from users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')), 
    path('', include('main.urls')),
    path('login', user_views.login_view, name='login'),
    path('register', user_views.register_view, name='register'),
    path('verify', user_views.verify_email_view, name='verify_email'),  # <-- ДОБАВИЛИ ЭТУ СТРОКУ
    path('logout', user_views.logout_view, name='logout'),
    path('profile', user_views.profile_view, name='profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=os.path.join(settings.BASE_DIR, 'assets'))
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static('/assets/', document_root=os.path.join(settings.BASE_DIR, 'assets'))