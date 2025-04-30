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
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import threading

User = get_user_model()

# Create your views here.


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=True)

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
                EmailThread(email).start()

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
    
class PasswordResetView(View):
    def get(self, request):    
        user = request.user
        email = user.email if user.is_authenticated else ''
        context = {'email': email}
        return render(request, 'authantications/password-reset.html', context)
    
    def post(self, request):
        email = request.POST.get('email', '').strip()

        if not validate_email(email):
            messages.error(request, 'Invalid email')
            return render(request, 'authantications/password-reset.html', {'email': email})
        
        user = User.objects.filter(email=email).first()
        if not user:
            messages.error(request, 'User with this email not found')
            return render(request, 'authantications/password-reset.html', {'email': email})

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = PasswordResetTokenGenerator().make_token(user=user)
        link = reverse('set-new-password', kwargs={'uid': uid, 'token': token})
        domain = get_current_site(request).domain
        password_reset_url = f"https://{domain}{link}"
        
        email = EmailMessage(
            subject = "Password Resent Link",
            body= f"Hello There\nUse this link to Reset your Finance tracker password\nlink: {password_reset_url}",
            from_email="noreply@semycolon.com",
            to=["irankundag65@gmail.com",]
        )
        EmailThread(email).start()
        # Here you would generate a token and send an email.
        messages.success(request, 'Password reset link sent to your email')
        return render(request, 'authantications/password-reset.html')

    
class CompletePasswordResetView(View):
    def get(self, request, uid, token):
        context = {
            'uid': uid,
            'token': token
        }
        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)
        except Exception:
            messages.info(request, "Something went wrong. Please try again.")
            return render(request, 'authantications/set-new-password.html', context)

        if not PasswordResetTokenGenerator().check_token(user, token):
            messages.info(request, "Oops! Link expired or invalid. Request a new one.")
            return render(request, 'authantications/password-reset.html', context)

        return render(request, 'authantications/set-new-password.html', context)

    def post(self, request, uid, token):
        context = {
            'uid': uid,
            'token': token,
            'data': request.POST
        }

        password1 = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')

        # Validate password strength
        password_errors = password_check(passwd=password1)
        if password_errors:
            for error in password_errors:
                messages.error(request, error)
            return render(request, 'authantications/set-new-password.html', context)

        # Check passwords match
        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return render(request, 'authantications/set-new-password.html', context)

        # Validate user and token again
        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)
        except Exception:
            messages.info(request, "Something went wrong. Please try again.")
            return render(request, 'authantications/set-new-password.html', context)

        if not PasswordResetTokenGenerator().check_token(user, token):
            messages.info(request, "Invalid or expired token. Try resetting again.")
            return redirect('password-reset')  # Or wherever your reset page is

        # Set the new password
        user.set_password(password1)
        user.save()

        messages.success(request, "Password reset successful! You can now log in.")
        return redirect('login')


