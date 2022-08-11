from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm,PasswordChangeForm,PasswordResetForm, SetPasswordForm
from .models import Profile



class UserUpdateForm(forms.ModelForm):
    email =forms.EmailField(max_length=40, widget=forms.EmailInput(attrs={ 'class' : 'form-control my-2', 'placeholder':'Email','readonly':True})) 
    username =forms.CharField(widget=forms.TextInput(attrs={ 'class' : 'form-control my-2', 'placeholder':'Username'}))
    first_name =forms.CharField(widget=forms.TextInput(attrs={ 'class' : 'form-control my-2', 'placeholder':'First Name'}))
    last_name =forms.CharField(widget=forms.TextInput(attrs={ 'class' : 'form-control my-2', 'placeholder':'Last Name'}), required=False)
    
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name'] 
    

class ProfileUpdateForm(forms.ModelForm):
    phone =forms.CharField(max_length=10, min_length=10, widget=forms.TextInput(attrs={ 'class' : 'form-control my-2','placeholder':'phone number','type':'number'}), required=False)
    DOB =forms.DateField(label='DOB', widget=forms.DateInput(attrs={ 'class' : 'form-control my-2','placeholder':'DD-MM-YYYY','type':'date','autoclose': True}), required=False)
    gender_choices=[('1','Male'),('2','Female'),('3','Dont want to specify')]
    gender =forms.ChoiceField(choices=gender_choices , widget=forms.Select(attrs={'class': 'form-control my-2'}))
    image=forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'custom-file-input my-1'}), required=False)

    class Meta:
        model = Profile
        fields = ['phone','DOB','gender','image']

class PasswordChangingForm(PasswordChangeForm):
    old_password =forms.CharField(label='Current password', max_length=30, widget=forms.PasswordInput(attrs={ 'class' : 'form-control my-3', 'placeholder':'Current Password','type':'password'})) 
    new_password1 =forms.CharField(max_length=100, label='New password', widget=forms.PasswordInput(attrs={ 'class' : 'form-control my-3', 'placeholder':'New Password','type':'password'}))
    new_password2 =forms.CharField(max_length=100, label='Confirm password', widget=forms.PasswordInput(attrs={ 'class' : 'form-control my-3', 'placeholder':'Confirm Password','type':'password'}))

    class Meta:
        model = User
        fields = ['old_password','new_password1','new_password2']

class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordResetForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control my-2','placeholder': 'Enter your Email','type': 'email','name': 'email'}))

    class Meta:
        fields=['email']


class PasswordResetingForm(SetPasswordForm):
    new_password1 =forms.CharField(max_length=100, label='New password', widget=forms.PasswordInput(attrs={ 'class' : 'form-control my-3', 'placeholder':'New Password','type':'password'}))
    new_password2 =forms.CharField(max_length=100, label='Confirm password', widget=forms.PasswordInput(attrs={ 'class' : 'form-control my-3', 'placeholder':'Confirm Password','type':'password'}))

    class Meta:
        model=User
        fields = ['new_password1','new_password2']
        

