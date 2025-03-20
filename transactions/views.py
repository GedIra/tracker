from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .models import Category, Expense, User
from users.models import Business, Employee
from django.contrib import messages
from django.shortcuts import redirect
from django.http import JsonResponse
from django.core.paginator import Paginator

# Create your views here.

@never_cache
@login_required(login_url='/auth/login/')
def index(request):
    user = request.user
    user_employers = user.employers.all()
    context = {
        "businesses": user_employers,
    }
    return render(request, 'expenses/index.html', context)

def business_expenses(request, business_id):
    business = Business.objects.get(id=business_id)
    expenses = business.expenses.all()[:3]  # Fetch only the first 3 expenses
    return render(request, 'business_expenses.html', {'business': business, 'expenses': expenses})


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
        "data" : request.POST
    }
    if request.method == 'GET':
        return render(request, 'expenses/add-expenses.html', context)
    
    if request.method == 'POST':
        amount = request.POST.get("amount")
        date = request.POST.get("date")
        category = request.POST.get("category")
        description = request.POST.get("description")
        name = request.POST.get("name")
        author = request.user


        if amount:
            amount = float(amount)
            if amount <= 0:
                messages.error(request, "Amount can't be negative or zero")
                return render(request, 'expenses/add-expenses.html', context)

        if not all([amount, date, category, name, description]):
            messages.error(request, "All fields are required is required")
            return render(request, 'expenses/add-expenses.html', context)
        
        
        # expense = Expense.objects.create(
        #     name = name,
        #     category = category,
        #     author = author,
        #     description = description,
        #     date = date
        # )

        messages.success(request,"Expense saved successfully")

        return redirect('expenses')
    return render(request, 'expenses/add-expenses.html', context)

@never_cache
@login_required(login_url='/auth/login/')
def expenseEditView(request, pk):
    user = request.user
    user_employers = user.employers.all()
    expense = Expense.objects.get(pk=pk)
    date = expense.date.strftime('%Y-%m-%d')

    context = {
        "data": expense,
        "date": date,
        "businesses": user_employers
    }

    if user == expense.author:
        if request.method == 'GET':
            return render(request, 'expenses/edit-expense.html', context)
    
        elif request.method == 'POST':
            amount = request.POST.get("amount")
            date = request.POST.get("date")
            category = request.POST.get("category")
            description = request.POST.get("description")
            name = request.POST.get("name")
            author = request.user


            if amount:
                amount = float(amount)
                if amount <= 0:
                    messages.error(request, "Amount can't be negative or zero")
                    return render(request, 'expenses/edit-expense.html', context)

            if not all([amount, date, category, name, description]):
                messages.error(request, "All fields are required is required")
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
    business = Business.objects.get(id=businessId)
    expenses = Expense.objects.filter(business= business) 
    business = business.name #to send the name only

    """Pagination"""
    paginator = Paginator(expenses, 5)  # Show 5 expenses per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj, #render a number of expenses available per page
        "business": business,
    }

    return render(request, 'expenses/business_expenses.html', context)






    