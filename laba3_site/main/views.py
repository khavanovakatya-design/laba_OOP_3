from django.shortcuts import render

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
    return render(request, 'collection-left-sidebar.html')

def contact(request):
    return render(request, 'contact.html')

def faq(request):
    return render(request, 'faq.html')

def login(request):
    return render(request, 'login.html')

def product(request):
    return render(request, 'product.html')

def register(request):
    return render(request, 'register.html')

def wishlist(request):
    return render(request, 'wishlist.html')