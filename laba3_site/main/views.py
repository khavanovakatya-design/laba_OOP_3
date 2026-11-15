from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Min, Max
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

    # 1. Получаем минимальную и максимальную цену из базы
    price_stats = products.aggregate(min_price=Min('price'), max_price=Max('price'))
    # Если товаров нет, ставим дефолтные значения
    absolute_min = int(price_stats['min_price'] or 0)
    absolute_max = int(price_stats['max_price'] or 10000)

    # 2. Получаем выбранные пользователем значения из URL (GET-запроса)
    current_min = request.GET.get('min_price')
    current_max = request.GET.get('max_price')

    # Если ползунки двигали, фильтруем товары
    if current_min and current_max:
        products = products.filter(price__gte=current_min, price__lte=current_max)
    else:
        # Если не двигали, ставим текущие значения равные крайним
        current_min = absolute_min
        current_max = absolute_max

    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'total_products': products.count(),
        'absolute_min': absolute_min,
        'absolute_max': absolute_max,
        'current_min': int(current_min),
        'current_max': int(current_max),
    }

    return render(request, 'collection-left-sidebar.html', context)

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