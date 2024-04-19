from django.forms import DateInput
from django_filters import FilterSet, ModelChoiceFilter, DateFilter, CharFilter

from .models import Post, Author


class PostFilter(FilterSet):
    title = CharFilter(
        lookup_expr='iregex',
        label='Заголовок',
        field_name='title'
    )

    author = ModelChoiceFilter(
        field_name='author',
        queryset=Author.objects.all(),
        label='Автор',
        empty_label='Все'
    )

    date = DateFilter(
        field_name='post_time',
        lookup_expr='gte',
        label='Дата публикации от',
        widget=DateInput(attrs={'type': 'date'}),
    )

    class Meta:
        model = Post
        fields = {}
