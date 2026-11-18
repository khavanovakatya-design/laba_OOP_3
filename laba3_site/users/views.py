from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from main.models import Product
from .models import Cart, CartItem
from django.http import JsonResponse

@login_required
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('profile')
        else:
            messages.error(request, 'Неверный логин или пароль')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def profile_view(request):
    return render(request, 'users/profile.html')

@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        quantity = int(request.POST.get('quantity', 1))

        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart, 
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not item_created:
            cart_item.quantity += quantity
            cart_item.save()

        # Если это AJAX-запрос, возвращаем JSON
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': f"Товар '{product.title}' добавлен в корзину!",
                'cart_total_items': cart.total_items # Общее количество товаров для счетчика в хедере
            })
            
        # Если обычный запрос - делаем редирект
        return redirect(request.META.get('HTTP_REFERER', 'collection'))
    
    return redirect('collection')

@login_required
def cart_view(request):
    # Получаем корзину текущего пользователя
    cart, created = Cart.objects.get_or_create(user=request.user)
    context = {
        'cart': cart, # Передаем в шаблон под именем 'cart'
    }
    # Передаем её в шаблон под именем 'cart'
    return render(request, 'cart.html', context)

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    messages.success(request, "Товар удален из корзины.")
    return redirect('cart')

@login_required
def update_cart(request, item_id):
    # Обновление количества (для кнопок + и -)
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    if quantity > 0:
        item.quantity = quantity
        item.save()
    else:
        item.delete()
    return redirect('cart')