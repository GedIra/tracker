from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from user_preferences.models import UserPreference

@receiver(post_save, sender=User)
def create_and_save_user_profile(sender, instance, created, **kwargs):
    """Automatically sets UserPrefrences when a new User is created."""
    if created:
        # Set UserPrefrences when a new User is created
        user_prefrences = UserPreference.objects.create(user=instance)

        # You can also save additional data here if needed
        user_prefrences.save()
