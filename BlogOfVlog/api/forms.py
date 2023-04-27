from django import forms
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from django.contrib.auth.models import User

class UserCreationForm(BaseUserCreationForm):
    email = forms.EmailField(required=True,help_text='Required. Enter the valid Email Address')
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ('username','email','first_name','last_name','password1','password2')