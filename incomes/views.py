from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from user_preferences.models import UserPreference
import json
from django.http import HttpResponse

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