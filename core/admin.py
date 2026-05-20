from django.contrib import admin
from core.models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'subject', 'created_at']
    search_fields = ['title','user']
    list_filter = ['subject']
    readonly_fields = ['user']


admin.site.register(Post, PostAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'user', 'body']
    search_fields = ['post','user']
    readonly_fields = ['user']

admin.site.register(Comment, CommentAdmin)