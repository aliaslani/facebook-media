import django_filters
from core.models import Post
from django import forms


class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains', label='Title', widget=forms.TextInput(attrs={'class': 'form-control'}))
    created_at_from = django_filters.DateFilter(field_name='created_at', lookup_expr='gte', label='From', widget=forms.DateInput(attrs={'type': 'date'}))
    created_at_to = django_filters.DateFilter(field_name='created_at', lookup_expr='lte', label='To', widget=forms.DateInput(attrs={'type': 'date'}))
    content = django_filters.CharFilter(field_name='content', lookup_expr='icontains', label='Content', widget=forms.TextInput(attrs={'type': 'text'}))

    class Meta:
        model = Post
        fields = ['title', 'created_at_from', 'created_at_to', 'content', 'subject']
