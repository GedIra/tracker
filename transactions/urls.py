from django.urls import path, include
from .views import (
    index, add_expenses, get_categories, expenseEditView, business_expenses, search_expenses
)
from django.views.decorators.csrf import csrf_exempt 


urlpatterns = [
    path('', index, name='expenses'),
    path("get-categories/<int:business_id>/", get_categories, name="get-categories"),
    path('add-expenses/', add_expenses, name='add-expenses'),
    path('edit-expense/<int:pk>/', expenseEditView, name="edit-expense"),
    path('<int:businessId>/expenses/', business_expenses, name="business-expenses"),
    path('search-expenses/', csrf_exempt(search_expenses), name='search-expenses'),
]
