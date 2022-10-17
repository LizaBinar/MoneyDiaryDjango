from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    profile_pic = models.ImageField(null=True, blank=True, verbose_name='Аватар', upload_to="images/profile/")
    facebook = models.CharField(max_length=50, null=True, blank=True)
    twitter = models.CharField(max_length=50, null=True, blank=True)
    instagram = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return str(self.user)


@receiver(post_save, sender=User)
def save_or_create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
