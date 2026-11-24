from .models import Cart, WishlistItem

def global_counts(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        return {
            'global_cart': cart,
            'global_wishlist_count': WishlistItem.objects.filter(user=request.user).count(),
        }
    return {
        'global_cart': None,
        'global_wishlist_count': 0,
    }