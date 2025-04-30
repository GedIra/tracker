from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from .models import Source, Income
from users.models import Business
from user_preferences.models import UserPreference
import json
from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.

@never_cache
@login_required(login_url='/auth/login/')
def index(request):
    user = request.user
    user_employers = user.employers.all()
    currency_str = UserPreference.objects.filter(user=user).first().currency
    currency = json.loads(currency_str.replace("'", "\""))  # Convert string to dictionary
    context = {
        "businesses": user_employers,
        "currency": currency['value']
    }
    return render(request, 'incomes/index.html', context)

def get_sources(request, business_id):
    sources = Source.objects.filter(company__id = business_id).values("id", "name")
    return JsonResponse(list(sources), safe=False)

@never_cache
@login_required(login_url='/auth/login/')
def add_incomes(request):
    user = request.user
    user_employers = user.employers.all()

    context = {
        "businesses": user_employers,
        "data": request.POST
    }

    if request.method == 'GET':
        return render(request, 'incomes/add-incomes.html', context)

    if request.method == 'POST':
        name = request.POST.get("name")
        amount = request.POST.get("amount")
        author = request.user
        business_id = request.POST.get("business")
        source_id = request.POST.get("source")
        description = request.POST.get("description")
        date = request.POST.get("date")
    
        if amount:
            try:
                amount = float(amount)
                if amount <= 0:
                    messages.error(request, "Amount can't be negative or zero")
                    return render(request, 'incomes/add-incomes.html', context)
            except ValueError:
                messages.error(request, "Amount must be a number")
                return render(request, 'incomes/add-incomes.html', context)

        if not all([amount, date, source_id, name, description]):
            messages.error(request, "All fields are required")
            return render(request, 'incomes/add-incomes.html', context)

        # ✅ Fetch the business and source objects
        business = get_object_or_404(Business, id=business_id)
        source = get_object_or_404(Source, id=source_id)

        income = Income.objects.create(
            name=name,
            amount=amount,
            author=author,
            business = business,
            source=source,
            description=description,
            date=date
        )

        messages.success(request, "Income saved successfully")
        return redirect('incomes')

    return render(request, 'incomes/add-incomes.html', context)

@never_cache
@login_required(login_url='/auth/login/')
def incomeEditView(request, pk):
    user = request.user
    income = get_object_or_404(Income, pk=pk, author=user)
    user_employers = user.employers.all()

    selected_business = income.business
    sources = Source.objects.filter(company=selected_business)

    context = {
        "data": income,
        "businesses": user_employers,
        "sources": sources
    }

    if request.method == 'GET':
        return render(request, 'incomes/edit-income.html', context)

    elif request.method == 'POST':
        name = request.POST.get("name")
        amount = request.POST.get("amount")
        business_id = request.POST.get("business")
        source_id = request.POST.get("source")
        description = request.POST.get("description")
        date = request.POST.get("date")

        if not all([amount, date, source_id, name, description]):
            messages.error(request, "All fields are required")
            return render(request, 'incomes/edit-income.html', context)

        business = get_object_or_404(Business, id=business_id)
        source = get_object_or_404(Source, id=source_id)

        try:
            amount = float(amount)
            if amount <= 0:
                messages.error(request, "Amount can't be negative or zero")
                return render(request, 'incomes/edit-income.html', context)
        except ValueError:
            messages.error(request, "Invalid amount")
            return render(request, 'incomes/edit-income.html', context)

        income.name = name
        income.amount = amount
        income.business = business
        income.source = source
        income.description = description
        income.date = date
        income.save()

        messages.success(request, "Income updated successfully")
        return redirect('incomes')

    return render(request, 'incomes/edit-income.html', context)

def business_incomes(request, businessId):
    user = request.user
    currency_str = UserPreference.objects.filter(user=user).first().currency
    currency = json.loads(currency_str.replace("'", "\""))  # Convert string to dictionary
    currency = currency['value']
    business = Business.objects.get(id=businessId)
    incomes = Income.objects.filter(business= business)
    business_name = business.name #to send the name only

    """Pagination"""
    paginator = Paginator(incomes, 5)  # Show 5 incomes per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj, #render a number of incomes available per page
        "business": business_name,
        "currency": currency
    }
    return render(request, 'incomes/business-incomes.html', context)

def search_incomes(request):
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

        incomes = Income.objects.filter(
            Q(business__in=businesses) & (
                Q(name__icontains=search_str) |
                Q(amount__startswith=search_str) |
                Q(source__name__icontains=search_str) |
                Q(description__icontains=search_str) |
                Q(date__istartswith=search_str)
            )
            
        )
        data = [
            {
                "name": str(income.name),
                "source": income.source.name,
                "id": income.id,
                "amount": float(income.amount),
                "date": str(income.date)
            }
            for income in incomes
        ] 
        return JsonResponse(data, safe=False)
    

