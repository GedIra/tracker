from django.urls import path
from  . views import index, add_expenses, get_categories, expenseEditView, business_expenses


urlpatterns = [
    path('', index, name='expenses'),
    path("get-categories/<int:business_id>/", get_categories, name="get-categories"),
    path('add-expenses/', add_expenses, name='add-expenses'),
    path('edit-expense/<int:pk>/', expenseEditView, name="edit-expense"),
    path('<int:businessId>/expenses/', business_expenses, name="business-expenses"),
]
