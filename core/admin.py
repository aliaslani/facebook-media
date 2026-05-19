from django.contrib import admin
from core.models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'subject', 'created_at']
    search_fields = ['title','user']
    list_filter = ['subject']
    readonly_fields = ['user']


admin.site.register(Post, PostAdmin)