import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.http import JsonResponse
from .forms import RegisterForm, LoginForm
from main.models import Product
from .models import Cart, CartItem, EmailVerification

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            code = str(random.randint(1000, 9999))
            EmailVerification.objects.create(user=user, code=code)

            subject = 'Код подтверждения регистрации'
            message = f'Здравствуйте!\n\nВаш код для завершения регистрации: {code}'
            
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
                request.session['verify_user_id'] = user.id
                return redirect('verify_email')
            except Exception as e:
                user.delete()
                messages.error(request, f'Ошибка отправки почты: {e}')
                return render(request, 'users/register.html', {'form': form})
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})

def verify_email_view(request):
    user_id = request.session.get('verify_user_id')
    if not user_id:
        return redirect('register')

    if request.method == 'POST':
        entered_code = request.POST.get('code')
        try:
            user = User.objects.get(id=user_id)
            verification = EmailVerification.objects.get(user=user)

            if verification.code == entered_code:
                user.is_active = True
                user.save()
                verification.delete()
                del request.session['verify_user_id']
                messages.success(request, 'Аккаунт подтвержден! Теперь вы можете войти.')
                return redirect('login')
            else:
                return render(request, 'users/verify_email.html', {'error': 'Неверный код'})
        except (User.DoesNotExist, EmailVerification.DoesNotExist):
            return redirect('register')

    return render(request, 'users/verify_email.html')

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

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': f"Товар '{product.title}' добавлен в корзину!",
                'cart_total_items': cart.total_items
            })
            
        return redirect(request.META.get('HTTP_REFERER', 'collection'))
    
    return redirect('collection')

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    context = {
        'cart': cart,
    }
    return render(request, 'cart.html', context)

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    messages.success(request, "Товар удален из корзины.")
    return redirect('cart')

@login_required
def update_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    if quantity > 0:
        item.quantity = quantity
        item.save()
    else:
        item.delete()
    return redirect('cart')

from .forms import PasswordResetRequestForm, PasswordResetConfirmForm
from .models import PasswordResetCode

def password_reset_request_view(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, "Пользователь с такой почтой не найден.")
                return render(request, 'users/password_reset_request.html', {'form': form})
            
            code = str(random.randint(1000, 9999))
            PasswordResetCode.objects.update_or_create(user=user, defaults={'code': code})

            subject = 'Сброс пароля'
            message = f'Здравствуйте!\n\nВаш код для сброса пароля: {code}'
            
            try:
                send_mail(
                    subject, message, settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False,
                )
                request.session['reset_user_id'] = user.id
                return redirect('password_reset_confirm')
            except Exception as e:
                messages.error(request, f'Ошибка отправки: {e}')
    else:
        form = PasswordResetRequestForm()
    return render(request, 'users/password_reset_request.html', {'form': form})

def password_reset_confirm_view(request):
    user_id = request.session.get('reset_user_id')
    if not user_id:
        return redirect('password_reset_request')

    if request.method == 'POST':
        form = PasswordResetConfirmForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            new_password = form.cleaned_data['new_password1']
            try:
                user = User.objects.get(id=user_id)
                reset_code = PasswordResetCode.objects.get(user=user)

                if reset_code.code == code:
                    user.set_password(new_password)
                    user.save()
                    reset_code.delete()
                    del request.session['reset_user_id']
                    messages.success(request, 'Пароль успешно изменен! Теперь вы можете войти.')
                    return redirect('login')
                else:
                    messages.error(request, "Неверный код.")
            except (User.DoesNotExist, PasswordResetCode.DoesNotExist):
                return redirect('password_reset_request')
    else:
        form = PasswordResetConfirmForm()
    
    return render(request, 'users/password_reset_confirm.html', {'form': form})