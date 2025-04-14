from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
User = get_user_model()

class UserPreference(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name="preferences")
    currency = models.TextField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.user)+ "'s" + " prefered currency"