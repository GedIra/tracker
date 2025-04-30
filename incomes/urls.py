from django.urls import path
from .views import (
    index, add_incomes, get_sources, incomeEditView, business_incomes, search_incomes
)
from django.views.decorators.csrf import csrf_exempt 

urlpatterns = [
    path('', index, name='incomes'),
    path('get-sources/<int:business_id>/', get_sources, name="get-sources"),
    path('add-incomes/', add_incomes, name='add-incomes'),
    path('edit-income/<int:pk>/', incomeEditView, name="edit-income"),
    path('<int:businessId>/incomes/', business_incomes, name="business-incomes"),
    path('search-incomes/', csrf_exempt(search_incomes), name='search-incomes'),
]
