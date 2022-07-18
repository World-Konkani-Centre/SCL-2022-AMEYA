from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from .models import Profile


class UserUpdateForm(forms.ModelForm):
    email =forms.EmailField(max_length=30, widget=forms.EmailInput(attrs={ 'class' : 'form-control my-2', 'placeholder':'Email','readonly':True})) 
    username =forms.CharField(widget=forms.TextInput(attrs={ 'class' : 'form-control my-2', 'placeholder':'Username'}))
    first_name =forms.CharField(widget=forms.TextInput(attrs={ 'class' : 'form-control my-2', 'placeholder':'First Name'}))
    last_name =forms.CharField(widget=forms.TextInput(attrs={ 'class' : 'form-control my-2', 'placeholder':'Last Name'}))
    
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name'] 
    

class ProfileUpdateForm(forms.ModelForm):
    phone =forms.CharField(max_length=10, min_length=10, widget=forms.TextInput(attrs={ 'class' : 'form-control my-2','placeholder':'phone number','type':'number'}))
    DOB =forms.DateField(label='DOB', widget=forms.DateInput(attrs={ 'class' : 'form-control my-2','placeholder':'DD-MM-YYYY','type':'date','autoclose': True}))
    gender_choices=[('1','Male'),('2','Female'),('3','Dont want to specify')]
    role_choices=[('1','User'),('2','Business')]
    gender =forms.ChoiceField(choices=gender_choices , widget=forms.Select(attrs={'class': 'form-control my-2'}))
    #role =forms.ChoiceField(choices=role_choices , widget=forms.Select(attrs={'class': 'form-control my-1'}))
    image=forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'custom-file-input my-1'}), required=False)

    class Meta:
        model = Profile
        fields = ['phone','DOB','gender','image']

