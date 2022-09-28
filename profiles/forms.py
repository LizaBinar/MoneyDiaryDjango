from django import forms
from django.core.exceptions import ValidationError

from .models import Profile


class ProfileFrom(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_pic'].empty_label = "Аватар профиля"

    class Meta:
        model = Profile
        fields = ['profile_pic']
        widgets = {
            'profile_pic': forms.FileInput(attrs={'class': 'form-control-file', 'verbose_name': "Красава молодец"}),
        }

