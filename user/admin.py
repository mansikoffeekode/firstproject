from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['pk', 'email', 'name', 'dob', 'is_active', 'is_superuser', 'is_staff', 'date_joined']
    search_fields = ['email', 'name']
    list_filter = ['is_superuser', 'is_staff', 'is_active']
    ordering = ['pk']
