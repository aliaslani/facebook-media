import django_tables2 as tables
from core.models import Post


class PostTable(tables.Table):
    class Meta:
        model = Post
        template_name = 'django_tables2/bootstrap5.html'
        fields = ('title', 'content', 'subject')


