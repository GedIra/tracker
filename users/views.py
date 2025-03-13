from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from django.views import View
import json
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.contrib import messages
from django.contrib.auth import get_user_model
from validate_email import validate_email
from .password_validator import password_check
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from users.utils import token_generator
from .forms import CustomLoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

User = get_user_model()

# Create your views here.


class RegisterView(View):
    def get(self, request):
        return render(request=request, template_name='authantications/register.html')
    
    def post(self,request):

        context = {
            "data" : request.POST
        }

        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST.get("password")
        password_errors = password_check(passwd=password)

        if not User.objects.filter(email=email).exists():
            if not User.objects.filter(username=username).exists():
                if password_errors:
                    for error in password_errors:
                        messages.error(request, error)  # Add each error to messages
                        return render(request=request, template_name='authantications/register.html', context=context) # Reload page to show errors
                
                user = User.objects.create_user(email=email, username=username, password=password)
                user.save()
                
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                subject = "Verify your account"
                token = token_generator.make_token(user=user)
                link = reverse('activate', kwargs={'uid': uid, 'token': token})
                domain = get_current_site(request).domain
                activate_url = f"https://{domain}{link}"
                
                body = f"Hello {username}\nUse this link to complete your Berwa Legacy Company account registration\nby clicking this link: {activate_url}"
                email = EmailMessage(
                    subject=subject,
                    body=body,
                    from_email="noreply@semycolon.com",
                    to=[email,]
                )
                email.send(fail_silently=True)

                messages.success(request,"Account created successfully")
                return render(request=request, template_name='authantications/register.html')
            
        return render(request=request, template_name='authantications/register.html')

class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data["username"]

        if not str(username).isalnum():
            return JsonResponse({"username_error":"The username must contain alphanumeric characters only !"}, status=400)
    
        if User.objects.filter(username=username).exists():
            return JsonResponse({"username_error": "This username is already taken !"}, status=409)
        return JsonResponse({"username": "Available"})
    
class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data["email"]

        if not validate_email(email):
            return JsonResponse({"email_error1": "Invalid email"}, status=400)
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({"email_error2" : "This email is already taken !"}, status=409)
        return JsonResponse({"email_valid": True})

class EmailVerficationView(View):
    def get(self, request, uid, token):

        try:
            uid = force_str(urlsafe_base64_decode(uid)) #getting user id again
            user = User.objects.get(pk=uid)
            
        except (User.DoesNotExist, ValueError, TypeError):
            return HttpResponseBadRequest('<h1>Invalid activation link</h1>')

        if not token_generator.check_token(user, token):
            return HttpResponseBadRequest('<h1>Bad request</h1>')
        
        if user.is_active:
            return redirect('login')

        user.is_active = True
        user.save()
        return redirect('register')
    
class  LoginView(View):
    def get(self,request):
        return render(request, 'authantications/login.html')
    
    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username and password:
            user = authenticate(request, username=username, password=password)

            if user:
                if user.is_active:
                    login(request=request, user=user)
                    messages.success(request, "Welcome again " + username)
                    return redirect('expenses')
        
                messages.error(request, "Please validate your account")
                return render(request, 'authantications/login.html')
            
            messages.error(request, "Invalid Username or Password")
            return render(request, 'authantications/login.html')

        return render(request, 'authantications/login.html')

class LogoutView(View):
    def post(self, request):
        logout(request)
        request.session.flush()  # ✅ Clears session data
        messages.success(request, "Successfully logged out, Login Again!")
        return redirect('login')
    



