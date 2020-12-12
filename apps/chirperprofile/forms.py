from django import forms

from .models import ChirperProfile

class ChirperProfileForm(forms.ModelForm):
    class Meta:
        model = ChirperProfile
        fields = ('avatar',)