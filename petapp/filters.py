import django_filters
from.models import Product
from django_filters import CharFilter

class ProductFilter(django_filters.FilterSet):
    product_name = CharFilter(field_name = 'product_name' , lookup_expr = 'icontains')
    class Meta:
        model = Product
        fields = ['product_name']