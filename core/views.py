from django.shortcuts import render
from core.models import Post, Comment
from django.views.generic import ListView, DetailView, CreateView, FormView
from core.forms import NewPostForm, CommentForm, Comment
from django_tables2 import SingleTableView
from core.tables import PostTable
from core.tables import CommentTable
from django.db.models import Count
class PostListView(ListView):
    model = Post
    template_name = 'core/post_list.html'
 
 
class PostDetail(DetailView):
    queryset = Post.objects.all()
    template_name = 'core/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.user = request.user
            comment.save()
            return self.get(request, *args, **kwargs)
        else:
            context = self.get_context_data(object=self.object)
            context['form'] = form
            return self.render_to_response(context)
    




# class NewPost(CreateView):
#     model = Post
#     fields = ['title','content', 'subject']
#     template_name = 'core/new_post.html'


# class NewPost(FormView):
#     form_class = NewPostForm
#     template_name = 'core/new_post.html'
#     success_url = '/posts/'

class NewPost(CreateView):
    model = Post
    form_class = NewPostForm
    template_name = 'core/new_post.html'
    success_url = '/posts/post/table/'

    def form_valid(self, form):

        form.instance.user = self.request.user
        return super().form_valid(form)


class PostTableView(SingleTableView):
    model = Post
    queryset = Post.objects.annotate(comments_count=Count('comments'))
    table_class = PostTable
    template_name = 'core/post_table.html'

    
class CommentTableView(SingleTableView):
    model = Comment
    template_name = 'core/comment_table.html'
    # paginator_class = LazyPaginator
    table_class = CommentTable
    paginate_by = 5