from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('p404', views.p404)
]
