from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .models import Category, Expense, User
from users.models import Business, Employee
from django.contrib import messages
from django.shortcuts import redirect
from django.http import JsonResponse
from django.core.paginator import Paginator
import json
from django.db.models import Q
from user_preferences.models import UserPreference


# Create your views here.

@never_cache
@login_required(login_url='/auth/login/')
def index(request):
    user = request.user
    user_employers = user.employers.all()
    preference = UserPreference.objects.filter(user=user).first()

    currency = {"name": "", "value": ""}  # fallback default

    if preference and preference.currency:
        try:
            currency = json.loads(preference.currency.replace("'", "\""))
        except json.JSONDecodeError:
            pass

    context = {
        "businesses": user_employers,
        "currency": currency['value']
    }
    return render(request, 'expenses/index.html', context)


def get_categories(request, business_id):
    categories = Category.objects.filter(company__id = business_id).values("id", "name")
    return JsonResponse(list(categories), safe=False)

@never_cache
@login_required(login_url='/auth/login/')
def add_expenses(request):
    user = request.user
    user_employers = user.employers.all()

    context = {
        "businesses": user_employers,
        "data": request.POST
    }

    if request.method == 'GET':
        return render(request, 'expenses/add-expenses.html', context)

    if request.method == 'POST':
        amount = request.POST.get("amount")
        date = request.POST.get("date")
        category_id = request.POST.get("category")
        description = request.POST.get("description")
        name = request.POST.get("name")
        author = request.user

        if amount:
            try:
                amount = float(amount)
                if amount <= 0:
                    messages.error(request, "Amount can't be negative or zero")
                    return render(request, 'expenses/add-expenses.html', context)
            except ValueError:
                messages.error(request, "Amount must be a number")
                return render(request, 'expenses/add-expenses.html', context)

        if not all([amount, date, category_id, name, description]):
            messages.error(request, "All fields are required")
            return render(request, 'expenses/add-expenses.html', context)

        # ✅ Fetch the category object
        category = get_object_or_404(Category, id=category_id)

        expense = Expense.objects.create(
            name=name,
            category=category,
            author=author,
            amount=amount,
            description=description,
            date=date
        )

        messages.success(request, "Expense saved successfully")
        return redirect('expenses')

    return render(request, 'expenses/add-expenses.html', context)

@never_cache
@login_required(login_url='/auth/login/')
def expenseEditView(request, pk):
    user = request.user
    user_employers = user.employers.all()
    expense = Expense.objects.get(pk=pk)

    context = {
        "data": expense,
        "businesses": user_employers
    }

    if user == expense.author:
        if request.method == 'GET':
            return render(request, 'expenses/edit-expense.html', context)
    
        elif request.method == 'POST':
            amount = request.POST.get("amount")
            date = request.POST.get("date")
            category_id = request.POST.get("category")
            description = request.POST.get("description")
            name = request.POST.get("name")
            author = request.user
            
            if category_id:
                id = int(category_id)
                category = Category.objects.get(id=id)

            if amount:
                amount = float(amount)
                if amount <= 0:
                    messages.error(request, "Amount can't be negative or zero")
                    return render(request, 'expenses/edit-expense.html', context)

            if not all([amount, date, category, name, description]):
                messages.error(request, "All fields are required")
                return render(request, 'expenses/edit-expense.html', context)
            
            expense.name = name
            expense.category = category
            expense.author = author
            expense.description = description
            expense.date = date
            messages.success(request,"Expense saved successfully")
            return redirect('expenses')
    return render(request, 'expenses/edit-expense.html', context)

def business_expenses(request, businessId):
    user = request.user
    currency_str = UserPreference.objects.filter(user=user).first().currency
    currency = json.loads(currency_str.replace("'", "\""))  # Convert string to dictionary
    currency = currency['value']
    business = Business.objects.get(id=businessId)
    expenses = Expense.objects.filter(business= business)
    business_name = business.name #to send the name only

    """Pagination"""
    paginator = Paginator(expenses, 5)  # Show 5 expenses per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj, #render a number of expenses available per page
        "business": business_name,
        "currency": currency
    }
    return render(request, 'expenses/business_expenses.html', context)

def search_expenses(request):
    user = request.user
    if request.method == 'POST':
        data = json.loads(request.body)
        search_str = data.get("searchStr", "").strip()
        business_name = data.get("business", "").strip()
        business = Business.objects.get(name=business_name)

        # Get business if provided, otherwise assign user’s businesses
        if business_name:
            business = Business.objects.filter(name=business_name).first()
            businesses = [business] if business else []
        else:
            businesses = user.employers.all()

        if not search_str:
            return JsonResponse([], safe=False)

        expenses = Expense.objects.filter(
            Q(business__in=businesses) & (
                Q(name__icontains=search_str) |
                Q(amount__startswith=search_str) |
                Q(category__name__icontains=search_str) |
                Q(description__icontains=search_str) |
                Q(date__istartswith=search_str)
            )
            
        )
        data = [
            {
                "name": str(expense.name),
                "category": expense.category.name,
                "id": expense.id,
                "amount": float(expense.amount),
                "date": str(expense.date)
            }
            for expense in expenses
        ] 
        return JsonResponse(data, safe=False)








    