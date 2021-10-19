from django_filters import CharFilter, FilterSet

from .views import Title


class CustomFilterSet(FilterSet):
    category = CharFilter(lookup_expr='icontains', field_name='category__slug')
    genre = CharFilter(lookup_expr='icontains', field_name='genre__slug')
    name = CharFilter(lookup_expr='icontains', field_name='name')

    class Meta:
        model = Title
        fields = ['name', 'year', 'category', 'genre']
