from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('p404', views.p404),
    path('about-us', views.about_us),
    path('article', views.article),
    path('blog', views.blog),
    path('cart', views.cart),
    path('checkout', views.checkout),
    path('collection', views.collection),
    path('contact', views.contact),
    path('faq', views.faq),
    path('login', views.login),
    path('product', views.product),
    path('register', views.register),
    path('wishlist', views.wishlist)
]
