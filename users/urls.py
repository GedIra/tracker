from django.urls import path
from django.views.generic import TemplateView
from .views import (UsernameValidationView, EmailValidationView, RegisterView,
                     EmailVerficationView, LoginView, LogoutView)
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signout/', LogoutView.as_view(), name='signout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('register/username-auth/', csrf_exempt(UsernameValidationView.as_view()), name="username-validation"),
    path('register/email-auth/', csrf_exempt(EmailValidationView.as_view()), name='email-validation'),
    path('activate/<uid>/<token>/', EmailVerficationView.as_view(), name='activate'),
]