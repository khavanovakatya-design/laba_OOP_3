from django.shortcuts import *
from django.core.paginator import Paginator
from django.db.models import Min, Max
from .models import Product
from .filters import ProductFilter

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

    # --- ЛОГИКА СОРТИРОВКИ ---
    sort_by = request.GET.get('sort', 'popular') # По умолчанию - популярность
    
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'name_asc':
        products = products.order_by('title')
    elif sort_by == 'name_desc':
        products = products.order_by('-title')
    # Для 'popular' ничего не делаем, остается базовый порядок из БД (по ID)
    # -----------------------------------------------------

    # 1. Получаем минимальную и максимальную цену для ползунка
    price_stats = products.aggregate(min_price=Min('price'), max_price=Max('price'))
    absolute_min = int(price_stats['min_price'] or 0)
    absolute_max = int(price_stats['max_price'] or 10000)

    # 2. Применяем фильтр
    product_filter = ProductFilter(request.GET, queryset=products)
    filtered_products = product_filter.qs

    # 3. Пагинация
    paginator = Paginator(filtered_products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    current_min = request.GET.get('price_min', absolute_min)
    current_max = request.GET.get('price_max', absolute_max)

    context = {
        'page_obj': page_obj,
        'total_products': filtered_products.count(),
        'filter': product_filter,
        'absolute_min': absolute_min,
        'absolute_max': absolute_max,
        'current_min': int(current_min) if current_min else absolute_min,
        'current_max': int(current_max) if current_max else absolute_max,
        'current_sort': sort_by, # <-- Передаем текущий тип сортировки в шаблон
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