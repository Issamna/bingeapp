from django.db import models
from .user import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(unique=True, max_length=100)


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        if "@" in instance.email:
            parse_username_from_email = instance.email.split("@")[0]
        else:
            parse_username_from_email = instance.email
        UserProfile.objects.create(user=instance, username=parse_username_from_email)
    instance.userprofile.save()


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()