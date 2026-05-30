from django.urls import path
from django.views.generic import TemplateView

from core.views import PostListView, PostDetail, NewPost,PostTableView, CommentTableView, UpdatePost, DeletePost,\
    BarChartView, PieChartView, PostSubmit, PostMonthlyReportView

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('post/new/', NewPost.as_view(), name='new_post'),
    path('post/table/', PostTableView.as_view(), name='post_table'),
    path('comments/table/', CommentTableView.as_view(), name='comment_table'),
    path('post/<int:pk>/update/', UpdatePost.as_view(), name='update_post'),
    path('post/<int:pk>/delete/', DeletePost.as_view(), name='delete_post'),
    path('chart/', TemplateView.as_view(template_name='core/charts.html'), name='chart'),
    path('chartJSON/', BarChartView.as_view(), name='bar_chart_json'),
    path('piechart/', PieChartView.as_view(), name='pie_chart_json'),
    path('piechart/', PieChartView.as_view(), name='pie_chart_json'),
    path('postsubmit/', PostSubmit.as_view(), name='post_submit'),
path(
    "reports/posts/monthly/",
    PostMonthlyReportView.as_view(),
    name="post_monthly_report"
),

]

