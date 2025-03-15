from django.contrib import admin
from .models import Expense, Category

# Register your models here.

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['name', 'business', 'category', 'author', 'amount']
    list_filter = ['category', 'author']
    ordering = ['name', 'category', 'amount']
    search_fields = ['name', 'category', 'author']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    ordering = ["name"]

