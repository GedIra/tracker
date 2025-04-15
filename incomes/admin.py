from django.contrib import admin
from .models import Income, Source

# Register your models here.

@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ['name', 'business', 'source', 'author', 'amount']
    list_filter = ['business', 'source', 'author']
    ordering = ['name', 'source', 'amount']
    search_fields = ['name', 'source__name__istartswith', 'author__username__istartswith', "date"]

@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ['name']
    ordering = ["name"]
