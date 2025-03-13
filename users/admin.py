from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Business, Employee, Category

# Register your models here.
User = get_user_model()

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active']
    sortable_by = ['username']
    list_filter = ['is_staff', 'is_superuser', 'is_active']
    search_fields = ['username', 'first_name', 'last_name']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    ordering = ["name"]

@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'owner', 'category']
    list_filter = ['owner', 'category', 'country']
    search_fields = ['name', 'owner', 'category', 'country']
    ordering = ['name']

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['employee__username', 'company__name', 'role', 'status']


