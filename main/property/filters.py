from django_filters import rest_framework as filters
from .models import Product


class ProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    min_quantity = filters.NumberFilter(field_name="quantity", lookup_expr='gte')
    max_quantity = filters.NumberFilter(field_name="quantity", lookup_expr='lte')
    category = filters.CharFilter(field_name="category", lookup_expr='exact')
    brand = filters.CharFilter(field_name="brand", lookup_expr='exact')
    rating = filters.NumberFilter(field_name="rating")
    created_at = filters.DateTimeFilter(field_name='created_at', lookup_expr='date')

    class Meta:
        model = Product
        fields = ['name', 'category', 'brand', 'min_price', 'max_price', 'min_quantity', 'max_quantity', 'rating',
                  'created_at']