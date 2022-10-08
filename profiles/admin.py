from django.contrib import admin
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'bio', 'profile_pic', 'facebook', 'twitter', 'instagram')
    list_display_links = ('id', 'user')
    search_fields = ('profile_pic', 'facebook', 'twitter', 'instagram')


admin.site.register(Profile, ProfileAdmin)
