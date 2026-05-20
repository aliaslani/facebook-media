from django.contrib import admin
from accounts.models import CustomUser, SocialLink


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email']
    search_fields = ['username','email']
    list_filter = ['is_active', 'is_superuser']


admin.site.register(CustomUser, CustomUserAdmin)


class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ['user', 'platform', 'url']
    search_fields = ['user__username', 'platform']
    list_filter = ['platform']

admin.site.register(SocialLink, SocialLinkAdmin)