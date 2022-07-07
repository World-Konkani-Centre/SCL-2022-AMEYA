
# forms.py
from django import forms

from base.models import Users

class UsersForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Users