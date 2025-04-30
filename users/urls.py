from django.urls import path
from django.views.generic import TemplateView
from .views import (UsernameValidationView, EmailValidationView, RegisterView,
                     EmailVerficationView, LoginView, LogoutView, PasswordResetView,
                     CompletePasswordResetView,)
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signout/', LogoutView.as_view(), name='signout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('register/username-auth/', csrf_exempt(UsernameValidationView.as_view()), name="username-validation"),
    path('register/email-auth/', csrf_exempt(EmailValidationView.as_view()), name='email-validation'),
    path('activate/<uid>/<token>/', EmailVerficationView.as_view(), name='activate'),
    path('get-password-reset-link/', PasswordResetView.as_view(), name='password-reset'),
    path('set-new-password/<uid>/<token>/', CompletePasswordResetView.as_view(), name='set-new-password'),
]