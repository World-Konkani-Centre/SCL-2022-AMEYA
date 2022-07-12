from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from .models import Profile


class UserUpdateForm(forms.ModelForm):
    email =forms.EmailField(max_length=30, widget=forms.EmailInput(attrs={ 'class' : 'form-control'}))
    username =forms.CharField(widget=forms.TextInput(attrs={ 'class' : 'form-control'}))
    first_name =forms.CharField(widget=forms.TextInput(attrs={ 'class' : 'form-control'}))
    last_name =forms.CharField(widget=forms.TextInput(attrs={ 'class' : 'form-control'}))
    
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name'] 
    




class ProfileUpdateForm(forms.ModelForm):
    phone =forms.CharField(max_length=10, widget=forms.TextInput(attrs={ 'class' : 'form-control'}))
    DOB =forms.DateField(widget=forms.DateInput(attrs={ 'class' : 'form-control'}))
    gender =forms.Select(attrs={ 'class' : 'form-control'})
    role =forms.Select(attrs={ 'class' : 'form-control'})   

    class Meta:
        model = Profile
        fields = ['phone','DOB','gender','role','image']

