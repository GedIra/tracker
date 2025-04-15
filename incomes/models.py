from django.db import models
from django.contrib.auth import get_user_model
import datetime
from users.models import Business, Employee

# Create your models here.

User = get_user_model()

class Income(models.Model):
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=19, decimal_places=10)
    author = models.ForeignKey(to=User, on_delete=models.RESTRICT, related_name='incomes')
    business = models.ForeignKey(Business, on_delete=models.RESTRICT, related_name='incomes')
    source = models.ForeignKey("Source", on_delete=models.RESTRICT)
    description = models.TextField(max_length=500)
    date = models.DateField(default=datetime.datetime.now)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.name} by {self.author} on {self.date}" 

class Source(models.Model):
    name = models.CharField(max_length=255)
    company = models.ForeignKey(to=Business, on_delete=models.RESTRICT, related_name="income_sources")


    class Meta:
        unique_together = ['company', 'name']

    def __str__(self):
        return f"{self.name}"