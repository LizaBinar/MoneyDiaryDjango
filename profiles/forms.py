from django import forms
from django.core.exceptions import ValidationError

from .models import Profile


class ProfileFrom(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_pic'].empty_label = "Аватар профиля"

    class Meta:
        model = Profile
        fields = ['profile_pic', 'bio', 'facebook', 'twitter', 'instagram']
        widgets = {
            'profile_pic': forms.FileInput(attrs={'class': 'form-control-file',}),
            'bio': forms.TextInput(attrs={'class': 'form-control', }),
            'facebook': forms.TextInput(attrs={'class': 'form-control', }),
            'twitter': forms.TextInput(attrs={'class': 'form-control', }),
            'instagram': forms.TextInput(attrs={'class': 'form-control', }),
        }
