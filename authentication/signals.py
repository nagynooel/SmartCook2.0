"""
    Signals for creating and changing profile pictures
    @package smartcook
    @author Noel Nagy
    @website: https://github.com/nagynooel
    ©2023 Noel Nagy - All rights reserved.
"""

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


# Create the profile object when User is created
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# Save the profile object when User is saved
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


# Set the default image if it has been removed
@receiver(post_save, sender=Profile)
def set_default_image(sender, instance, **kwargs):
    if not instance.picture:
        instance.picture = Profile.picture.field.upload_to + "default.svg"
        instance.save()