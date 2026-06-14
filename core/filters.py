import django_filters
from accounts.models import Contact
from core.models import Post
from django import forms


class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='contains', label='Title',
                                      widget=forms.TextInput(attrs={'class': 'form-control'}))
    created_at_from = django_filters.DateFilter(field_name='created_at', lookup_expr='gte', label='From',
                                                widget=forms.DateInput(attrs={'type': 'date'}))
    created_at_to = django_filters.DateFilter(field_name='created_at', lookup_expr='lte', label='To',
                                              widget=forms.DateInput(attrs={'type': 'date'}))
    content = django_filters.CharFilter(field_name='content', lookup_expr='contains', label='Content', widget=forms.TextInput(attrs={'type': 'text'}))
    subject = django_filters.CharFilter(field_name='subject', lookup_expr='contains', label='Subject', widget=forms.TextInput(attrs={'class': 'form-control'}))

    username = django_filters.CharFilter(
        field_name='user__username',
        lookup_expr='contains',
        label='Author'
    )


    class Meta:
        model = Post
        fields = ['title', 'content', 'subject', 'created_at_from', 'created_at_to', 'username']


class ContactFilter(django_filters.FilterSet):
    subject = django_filters.CharFilter(field_name='subject', lookup_expr='icontains', label='Subject',
                                        widget=forms.TextInput(attrs={'class': 'form-control'}))
    sender = django_filters.CharFilter(field_name='sender', lookup_expr='icontains', label='From',
                                       widget=forms.TextInput(attrs={'class': 'form-control'}))
    created_at_from = django_filters.DateFilter(field_name='created_at', lookup_expr='gte', label='From',
                                                widget=forms.DateInput(attrs={'type': 'date'}))
    created_at_to = django_filters.DateFilter(field_name='created_at', lookup_expr='lte', label='To',
                                              widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Contact
        fields = ['subject', 'sender']
