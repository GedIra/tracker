from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .models import Category, Expense, User
from users.models import Business, Employee
from django.contrib import messages
from django.shortcuts import redirect
from django.http import JsonResponse



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


def get_categories(request, business_id):
    categories = Category.objects.filter(company__id = business_id).values("id", "name")
    return JsonResponse(list(categories), safe=False)

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
    