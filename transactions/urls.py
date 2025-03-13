from django.urls import path
from  . views import index, add_expenses, get_categories


urlpatterns = [
    path('', index, name='expenses'),
    path("get-categories/<int:business_id>/", get_categories, name="get_categories"),
    path('add-expenses/', add_expenses, name='add-expenses'),
]
