from django.contrib import admin
from .models import UserPreference

# Register your models here.

@admin.register(UserPreference)
class UserPrefrenceAdmin(admin.ModelAdmin):
    list_display = ['user__username', 'currency']
    list_filter = ['currency']
    ordering = ['user__username']
