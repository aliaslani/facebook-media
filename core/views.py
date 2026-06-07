import json
from itertools import count

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator


from core.filters import PostFilter
from core.models import Post, Comment, HxPost
from django.views.generic import ListView, DetailView, CreateView, FormView, UpdateView, DeleteView
from core.forms import NewPostForm, CommentForm, Comment, HxPostForm
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
from braces.views import RecentLoginRequiredMixin
from braces.views import FormInvalidMessageMixin
from django_ratelimit.decorators import  ratelimit
from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse
from django.db.models import F
from rest_framework.viewsets import ModelViewSet
from core.serializers import PostSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from core.utils import DevExtremePagination
from rest_framework import status
from rest_framework.response import Response
from core.models import SubjectChoice
from django.views.decorators.csrf import csrf_exempt

def subject_choices(request):
    data = [
        {
            "value": value,
            "text": label
        } for value, label in SubjectChoice.choices
    ]
    return JsonResponse(data, safe=False)
# class PostListView(ListView):
#     model = Post
#     template_name = 'core/post_list.html'
#     context_object_name = 'posts'
#     paginate_by = 20
def ratelimited_error(request, exception=None):
    return render(
        request,
        "core/429.html",
        status=429,
    )

class PostViewSet(ModelViewSet):
    queryset = Post.objects.select_related('user').annotate(username=F("user__username"))
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = PostFilter
    search_fields = ['title', 'content', 'subject']
    pagination_class = DevExtremePagination

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()

        print("PATCH DATA:", request.data)

        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=True
        )

        if not serializer.is_valid():
            print("ERRORS:", serializer.errors)
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()

        return Response(serializer.data)
@method_decorator(ratelimit(key='ip', rate='5/m', block=True), name='dispatch')
class PostListView(RecentLoginRequiredMixin, FilterView):
    model = Post
    template_name = 'core/post_list.html'
    filterset_class = PostFilter
    context_object_name = 'posts'
    paginate_by = 5
    max_last_login_delta = 600000000
    raise_exception = True
class PostJsonView(View):
    def get(self, request, pk=None, *args, **kwargs):
        if pk:
            post = get_object_or_404(Post, pk=pk)
            return JsonResponse({
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "created_at": post.created_at,
                "user": post.user.username,
            })

        data = list(
            Post.objects.annotate(username=F("user__username")).values(
                "id",
                "title",
                "content",
                "subject",
                "created_at",
                "username",
            )
        )
        return JsonResponse(data, safe=False)
    def post(self, request, *args, **kwargs):
        try:
            payload = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse(
                {"error": "Invalid JSON"},
                status=400
            )
        post = Post.objects.create(
            title=payload["title"],
            content=payload["content"],
            user=request.user,
        )
        return JsonResponse(
            {
             'id': post.id,
             'message': 'created successfully',
             }
        )
    def put(self, request, *args, **kwargs):
        try:
            payload = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse(
                {"error": "Invalid JSON"},
                status=400
            )
        post_id = payload["id"]
        post = Post.objects.get(id=post_id)
        post.title = payload.get("title") or post.title
        post.content = payload.get("content") or post.content
        post.save()
        return JsonResponse(
            {
                "message": "updated successfully",
            }
        )
    def delete(self, request, *args, **kwargs):
        try:
            payload = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse(
                {"error": "Invalid JSON"},
                status=400
            )
        post_id = payload["id"]
        Post.objects.filter(id=post_id).delete()
        return JsonResponse(
            {
                "message": "deleted successfully",
            }
        )
def dev_post_list(request):
    config = {"pageSize": 20, "pageTitle": "Post List DevExpress"}
    return render(request, "core/devexpress.html", {"config": json.dumps(config)})
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

class NewPost(FormInvalidMessageMixin, CreateView):
    model = Post
    form_class = NewPostForm
    template_name = 'core/new_post.html'
    success_url = reverse_lazy('post_table')
    form_invalid_message = "Oops, something went wrong."


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

class TotalNumberPostField(ComputationField):
    calculation_method = Count
    calculation_field = "id"
    verbose_name = "Total number of posts"
    name = "total_count"
class PostSubmit(ReportView):
    template_name = "core/post_per_user_chart.html"
    report_model = Post
    date_field = "created_at"
    group_by = "user__username"
    # crosstab_field = "subject"
    # crosstab_columns = [
    #     TotalNumberPostField,
    # ]
    # crosstab_ids = ["social","sport"]
    # crosstab_compute_remainder = True
    # template_name = "core/post_per_user_chart.html"
    columns = [
        "user__username",


        ComputationField.create(
            Count,
            "id",
            name="subject_count",
            verbose_name="Number of posts",
        )
    ]

    chart_settings = [
        Chart(
            "Number of posts",
            Chart.COLUMN,
            data_source=["subject_count"],
            title_source=["user__username"]
        )
    ]



class PostMonthlyReportView(ReportView):
    template_name = 'core/post_per_month_chart.html'
    report_model = Post
    date_field = "created_at"
    group_by = "user__username"
    time_series_pattern = "monthly"
    time_series_columns = [
        TotalNumberPostField,
    ]

    columns = [
        "user__username",

    ComputationField.create(
            Count,
            "id",
            name="post_count",
            verbose_name="Number of posts",
        )
    ]
    chart_settings = [
        Chart(
            "Post Per Month",
            Chart.BAR,
            data_source=["total_count"],
            title_source=["user__username"],
        ),
        Chart(
            "Post Monthly [Bar]",
            Chart.COLUMN,
            data_source=["total_count"],
            title_source=["user__username"],
        )
    ]

def post_list(request):
    context = get_paginated_posts(request)
    if request.htmx:
        return render(request, "posts/_table.html", context)

    return render(request, "posts/list.html", context)

def post_create(request):
    form = HxPostForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()

            if request.htmx:
                context = get_paginated_posts(request)
                return render(
                    request,
                    "posts/_table.html",
                    context
                )

            return redirect("post-list")

    template = (
        "posts/_modal_form.html"
        if request.htmx
        else "posts/create_post.html"
    )

    return render(request, template, {
        "form": form
    })

def post_edit(request, pk):
    post = get_object_or_404(HxPost, pk=pk)

    form = HxPostForm(request.POST or None, instance=post)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            context = get_paginated_posts(request)
            return render(
                request,
                "posts/_table.html",
                context
            )

        return render(
            request,
            "posts/_modal_form.html",
            {
                "form": form,
                "post": post
            }
        )

    return render(
        request,
        "posts/_modal_form.html",
        {
            "form": form,
            "post": post
        }
    )
def post_inline_update(request, pk):
    post = get_object_or_404(HxPost, pk=pk)

    title = request.POST.get("title", "").strip()

    if title and title != post.title:
        post.title = title
        post.save()

    return render(
        request,
        "posts/_title_cell.html",
        {"post": post}
    )
def get_paginated_posts(request):
    qs = HxPost.objects.all().order_by("-created_at")

    search = request.GET.get("search")
    status = request.GET.get("status")

    if search:
        qs = qs.filter(title__icontains=search)

    if status:
        qs = qs.filter(status=status)

    paginator = Paginator(qs, 5)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return {
        "posts": page_obj.object_list,
        "page_obj": page_obj,
    }