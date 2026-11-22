from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('p404', views.p404, name='p404'),
    path('about-us', views.about_us, name='about_us'),
    path('article', views.article, name='article'),
    path('blog', views.blog, name='blog'),
    path('collection', views.collection, name='collection'),
    path('contact', views.contact, name='contact'),
    path('faq', views.faq, name='faq'),
    path('product/<int:product_id>/', views.product, name='product_detail'),
    path('wishlist', views.wishlist, name='wishlist'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('offer/', views.offer, name='offer'),
]