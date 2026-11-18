from .models import Cart

def cart_processor(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        return {'global_cart': cart}
    return {'global_cart': None}