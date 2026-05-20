from django.urls import path
from core.views import PostListView, PostDetail, NewPost,PostTableView, CommentTableView, UpdatePost, DeletePost

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('post/new/', NewPost.as_view(), name='new_post'),
    path('post/table/', PostTableView.as_view(), name='post_table'),
    path('comments/table/', CommentTableView.as_view(), name='comment_table'),
    path('post/<int:pk>/update/', UpdatePost.as_view(), name='update_post'),
    path('post/<int:pk>/delete/', DeletePost.as_view(), name='delete_post'),

]

