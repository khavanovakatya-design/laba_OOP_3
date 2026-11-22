from .models import Cart, WishlistItem

def cart_processor(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        return {'global_cart': cart}
    return {'global_cart': None}

def wishlist_count(request):
    if request.user.is_authenticated:
        return {'wishlist_count': WishlistItem.objects.filter(user=request.user).count()}
    return {'wishlist_count': 0}