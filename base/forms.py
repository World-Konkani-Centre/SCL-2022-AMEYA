from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from .models import Profile

class UserUpdateForm(forms.ModelForm):
    email =forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email','first_name','last_name'] 



class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone','DOB','gender','role','image']

