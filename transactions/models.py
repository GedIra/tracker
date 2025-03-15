from django.db import models
from django.contrib.auth import get_user_model
import datetime
from users.models import Business, Employee

# Create your models here.

User = get_user_model()

class Expense(models.Model):
    name = models.CharField(max_length=255)
    amount = models.IntegerField()
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='expenses')
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='expenses')
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    description = models.TextField(max_length=500)
    date = models.DateField(default=datetime.datetime.now)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.name} by {self.author} on {self.date}" 

class Category(models.Model):
    company = models.ForeignKey(to=Business, on_delete=models.CASCADE, related_name="expense_categories")
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Categories'
        unique_together = ['company', 'name']

    def __str__(self):
        return f"{self.name}"


