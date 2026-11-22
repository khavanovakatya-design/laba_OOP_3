from django.shortcuts import *
from django.core.paginator import Paginator
from django.db.models import Min, Max
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
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
    sort_by = request.GET.get('sort', 'popular')
    
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'name_asc':
        products = products.order_by('title')
    elif sort_by == 'name_desc':
        products = products.order_by('-title')

    price_stats = products.aggregate(min_price=Min('price'), max_price=Max('price'))
    absolute_min = int(price_stats['min_price'] or 0)
    absolute_max = int(price_stats['max_price'] or 10000)

    product_filter = ProductFilter(request.GET, queryset=products)
    filtered_products = product_filter.qs

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
        'current_sort': sort_by,
    }

    return render(request, 'collection-left-sidebar.html', context)

def contact(request):
    return render(request, 'contact.html')

def faq(request):
    return render(request, 'faq.html')

def product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    related_products = Product.objects.exclude(id=product.id).order_by('?')[:8]
    return render(request, 'product.html', {'product': product, 'related_products': related_products})

def wishlist(request):
    return render(request, 'wishlist.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            return render(request, 'users/register.html', {'error': 'Пароли не совпадают'})

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()

        subject = 'Подтверждение регистрации'
        message = f'Здравствуйте, {username}!\n\nВы успешно зарегистрировались на нашем сайте. Ваш логин: {username}.'
        
        domain = email.split('@')[-1].lower()
        
        if 'gmail' in domain:
            mail_backend = 'gmail'
        elif 'yandex' in domain:
            mail_backend = 'yandex'
        elif 'mail.ru' in domain or 'bk.ru' in domain or 'list.ru' in domain or 'inbox.ru' in domain:
            mail_backend = 'mailru'
        else:
            mail_backend = 'default'

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
            using=mail_backend,
        )

        return redirect('login') 

    return render(request, 'users/register.html')

from django.shortcuts import render

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def offer(request):
    return render(request, 'offer.html')