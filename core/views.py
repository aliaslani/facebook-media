from itertools import count

from django.shortcuts import render

from core.filters import PostFilter
from core.models import Post, Comment
from django.views.generic import ListView, DetailView, CreateView, FormView, UpdateView, DeleteView
from core.forms import NewPostForm, CommentForm, Comment
from django_tables2 import SingleTableView, SingleTableMixin
from core.tables import PostTable
from core.tables import CommentTable
from django.db.models import Count
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django_filters.views import FilterView
from core.filters import PostFilter
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView
from chartjs.views.columns import BaseColumnsHighChartsView
from chartjs.views.pie import HighChartPieView
from accounts.models import CustomUser
from django.db.models import Count
from core.filters import PostFilter
from slick_reporting.views import ReportView, Chart
from slick_reporting.fields import ComputationField




# class PostListView(ListView):
#     model = Post
#     template_name = 'core/post_list.html'
#     context_object_name = 'posts'
#     paginate_by = 20


class PostListView(FilterView):
    model = Post
    template_name = 'core/post_list.html'
    filterset_class = PostFilter
    context_object_name = 'posts'
    paginate_by = 5

 
class PostDetail(DetailView):
    model = Post
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
    




# class NewPost(FormView):
#     form_class = NewPostForm
#     template_name = 'core/new_post.html'
#     success_url = '/posts/'

class NewPost(CreateView):
    model = Post
    form_class = NewPostForm
    template_name = 'core/new_post.html'
    success_url = reverse_lazy('post_table')

    def form_valid(self, form):

        form.instance.user = self.request.user
        return super().form_valid(form)


class PostTableView(SingleTableMixin, FilterView):
    model = Post
    queryset = Post.objects.annotate(comments_count=Count('comments'))
    table_class = PostTable
    filterset_class = PostFilter
    template_name = 'core/post_table.html'

    
class CommentTableView(SingleTableView):
    model = Comment
    template_name = 'core/comment_table.html'
    table_class = CommentTable
    paginate_by = 5


class UpdatePost(UpdateView, LoginRequiredMixin, UserPassesTestMixin):
    model = Post
    form_class = NewPostForm
    template_name = 'core/edit_post.html'
    success_url = reverse_lazy('post_table')


class DeletePost(DeleteView, LoginRequiredMixin, UserPassesTestMixin):
    model = Post
    success_url = reverse_lazy('post_table')


class BarChartView(BaseColumnsHighChartsView):
    def get_labels(self):
        return list(CustomUser.objects.values_list('username', flat=True))

    def get_data(self):
        qs = CustomUser.objects.annotate(post_count=Count('posts'))
        return [[u.post_count for u in qs ]]



class PieChartView(HighChartPieView):
    def get_labels(self):
        return list(CustomUser.objects.values_list('username', flat=True))
    def get_data(self):
        qs = CustomUser.objects.annotate(post_count=Count('posts'))
        return [[u.post_count for u in qs]]


class PostSubmit(ReportView):
    report_model = Post
    date_field = 'created_at'
    group_by = 'user'

    columns = [
        'username',
        ComputationField.create(
            method=Count, field="title", name="title__count", verbose_name="Number of posts"
        ),
    ]
    chart_settings = [
        Chart(
            "Number of posts",
            Chart.BAR,
            data_source=['count__title'],
            title_source=['user']
        ),
        Chart(
            "Number of comments [PIE]",
            Chart.PIE,
            data_source=['count__title'],
            title_source=['user']
        )
    ]