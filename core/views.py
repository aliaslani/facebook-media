from django.shortcuts import render
from core.models import Post
from django.views.generic import ListView, DetailView, CreateView, FormView
from core.forms import NewPostForm
from django_tables2 import SingleTableView
from core.tables import PostTable

class PostListView(ListView):
    model = Post
    template_name = 'core/post_list.html'
 
 
class PostDetail(DetailView):
    queryset = Post.objects.all()


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
    table_class = PostTable
    template_name = 'core/post_table.html'


