from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import User, UserProfile
import logging


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        logging.info(f"User Profile is created successfully")
    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
            logging.info(f"User Profile is updated successfully")
        except:
            UserProfile.objects.create(user=instance)
            logging.info(f"User Profile Does not Exist, but created successfully")
        print("User is Updated")


@receiver(pre_save, sender=User)
def pre_save_profile_receiver(sender, instance, **kwargs):
    pass