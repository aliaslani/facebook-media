from django.contrib import admin
from accounts.models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email']
    search_fields = ['username','email']
    list_filter = ['is_active', 'is_superuser']


admin.site.register(CustomUser, CustomUserAdmin)

