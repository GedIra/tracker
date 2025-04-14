from django.shortcuts import render
from .models import User, UserPreference
import os, json
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages


# Create your views here.
@never_cache
@login_required(login_url='/auth/login/')
def index(request):
    user = request.user 
    preference = UserPreference.objects.filter(user=user).first()
    currency = json.loads(preference.currency.replace("'", "\""))  # Convert string to dictionary

    currency_data = []
    file_path =os.path.join(settings.BASE_DIR, 'currencies.json')
    with open(file_path, 'r') as file:
        data = json.load(file)
        for key, value in data.items():
            currency_data.append({"name": key, "value": value})

    
    if request.method == 'POST':
        currency_str = request.POST.get("currency")
        currency = json.loads(currency_str.replace("'", "\""))  # Convert string to dictionary
        preference.currency = currency
        preference.save()
        messages.success(request, f'{currency["name"]} Saved successfully')
        return render(request, "preferences/index.html", {"currencies": currency_data, "preffered": currency})
    
    return render(request, "preferences/index.html", {"currencies": currency_data, "preffered": currency})


  