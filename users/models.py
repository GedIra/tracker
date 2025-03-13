from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth import get_user_model
from django_countries.fields import CountryField

# Create your models here.

class CustomUserManager(BaseUserManager):
  def create_user(self, username, email, password=None):
    if not email:
      raise ValueError("The email is required")

    if not password: 
      raise ValueError("Password is required")

    email = self.normalize_email(email=email)
    user = self.model(username=username, email=email)
    user.set_password(password)
    user.is_active = False
    user.save(using = self._db)
    return user

  def create_superuser(self, username, email, password=None):
    user = self.create_user(username, email=email, password=password)
    user.is_active = True
    user.is_staff = True
    user.is_superuser = True
    user.save(using=self._db)
    return user

class CustomUser(AbstractUser):
  email = models.EmailField(verbose_name="email address", unique=True, max_length=255)
  REQUIRED_FIELDS = ['email']
  objects = CustomUserManager()
  
  def __str__(self):
    return self.username

User = get_user_model()

class Category(models.Model):
  name = models.CharField(max_length=255, unique=True)

  class Meta:
    verbose_name_plural = 'Categories'

  def __str__(self):
    return f"{self.name}"

class Business(models.Model):
  name = models.CharField(max_length=255)
  country = CountryField()
  owner = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='businesses')
  employees = models.ManyToManyField(to=User, through="Employee", related_name="employers")
  category = models.ForeignKey(Category, models.SET_NULL, null=True, blank=True, related_name="businesses")
  description = models.TextField(max_length=1000)

  class Meta:
    unique_together = ['name', 'owner']
    verbose_name_plural = 'businesses'

  def __str__(self):
    return self.name
  

class Employee(models.Model):
  choices = [
    ("active", "Is active"),
    ("onhold", "Is onhold"),
    ("anctive", "Is inactive")
  ]
  roles = [
    ("manager", "Manger"),
    ("secreatary", "Secreatary"),
    ("cashier", "bookkeeper")
  ]
  employee = models.ForeignKey(User, on_delete=models.CASCADE)
  company = models.ForeignKey(Business, on_delete=models.CASCADE)
  role = models.CharField(max_length=10, choices=roles)
  status = models.CharField(max_length=7, choices=choices)

  class Meta:
    verbose_name_plural = 'employees'
    unique_together = ['employee', 'company']

  def __str__(self):
    return f'{self.employee.username}'