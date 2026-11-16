import django_filters
from .models import *

class ProductFilter(django_filters.FilterSet):
    # Фильтр по цене (от и до)
    price_min = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name="price", lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['category', 'vendor', 'metal', 'color', 'size']