from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save, sender=User)
def manage_user_profile(sender, instance, created, **kwargs):
    if created:
        # Since fields are null=True, we only need to pass the user instance!
        UserProfile.objects.create(user=instance)
    else:
        # Safeguard: Save the profile if it exists when the User object updates
        if hasattr(instance, 'userprofile'):
            instance.userprofile.save()
