from django.urls import path
from core.views import PostListView, PostDetail, NewPost,PostTableView

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('post/new/', NewPost.as_view(), name='new_post'),
    path('post/table/', PostTableView.as_view(), name='post_table'),
]

