from django.shortcuts import render, get_object_or_404
from .models import Product

def index(request):
    return render(request, 'index.html')

def p404(request):
    return render(request, '404.html')

def about_us(request):
    return render(request, 'about-us.html')

def article(request):
    return render(request, 'article.html')

def blog(request):
    return render(request, 'blog.html')

def cart(request):
    return render(request, 'cart.html')

def checkout(request):
    return render(request, 'checkout.html')

def collection(request):
    products = Product.objects.all()
    return render(request, 'collection-left-sidebar.html', {'products': products})

def contact(request):
    return render(request, 'contact.html')

def faq(request):
    return render(request, 'faq.html')

def login(request):
    return render(request, 'login.html')

def product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    related_products = Product.objects.exclude(id=product.id).order_by('?')[:8]
    return render(request, 'product.html', {'product': product, 'related_products': related_products})

def register(request):
    return render(request, 'register.html')

def wishlist(request):
    return render(request, 'wishlist.html')