import django_tables2 as tables
from core.models import Post, Comment

class PostTable(tables.Table):

    comments_count = tables.Column(verbose_name='Comments Count', empty_values=(), orderable=True)
    title = tables.LinkColumn('post_detail', args=[tables.A('pk')], verbose_name='Title')
    class Meta:
        model = Post
        template_name = 'django_tables2/bootstrap5.html'
        fields = ('title', 'content', 'subject')
        

    def render_content(self, value):
        return value[:10] + '...' if len(value) > 10 else value

class CommentTable(tables.Table):

    class Meta:
        model = Comment
        template_name = 'django_tables2/bootstrap5.html'
        fields = ('post', 'user', 'body', 'created_at')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_columns['post'].verbose_name = 'Post Title'
        self.base_columns['user'].verbose_name = 'Comment Author'
        self.base_columns['body'].verbose_name = 'Comment Body'
        self.base_columns['created_at'].verbose_name = 'Created At'
        paginate_by = 2