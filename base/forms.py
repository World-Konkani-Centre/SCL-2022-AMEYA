from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from .models import Profile


class UserUpdateForm(forms.ModelForm):
    email =forms.EmailField(max_length=30, widget=forms.EmailInput(attrs={ 'class' : 'form-control', 'placeholder':'Email'})) 
    username =forms.CharField(widget=forms.TextInput(attrs={ 'class' : 'form-control', 'placeholder':'Username'}))
    first_name =forms.CharField(widget=forms.TextInput(attrs={ 'class' : 'form-control', 'placeholder':'First Name'}))
    last_name =forms.CharField(widget=forms.TextInput(attrs={ 'class' : 'form-control', 'placeholder':'Last Name'}))
    
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name'] 
    




class ProfileUpdateForm(forms.ModelForm):
    phone =forms.CharField(max_length=10, min_length=10, widget=forms.TextInput(attrs={ 'class' : 'form-control','placeholder':'phone number','type':'number'}))
    DOB =forms.DateField(widget=forms.DateInput(attrs={ 'class' : 'form-control','placeholder':'DD-MM-YYYY','type':'date','autoclose': True}))
    gender =forms.Select(attrs={'class': 'form-control'})
    role =forms.Select(attrs={ 'class' : 'form-control'})   

    class Meta:
        model = Profile
        fields = ['phone','DOB','gender','role','image']

