from django.contrib import admin
from .models import Cart, CartItem

# Регистрируем корзину
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'total_price', 'total_items')
    search_fields = ('user__username',)

# Регистрируем товары в корзине
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'total_price')
    list_filter = ('cart__user',)
    search_fields = ('product__title',)