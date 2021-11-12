from django import forms
from .models import UserProfile


class ProfileForm(forms.ModelForm):
    contact = forms.IntegerField(label='', widget=forms.NumberInput(
        attrs={
            'placeholder': 'Contact Number'
        }
    ))

    name = forms.CharField(label='', widget=forms.TextInput(
        attrs={
            'placeholder': 'Enter Your Name'
        }
    ))

    class Meta:
        model = UserProfile
        fields = [
            'profile_image',
            'name',
            'bio',
            'contact',
            'organizer'
        ]
