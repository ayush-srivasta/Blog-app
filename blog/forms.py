from django import forms
from django.contrib.auth import models
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User
from django.db.models import fields
from .models import Comments

class SignupForm(UserCreationForm):
    first_name=forms.CharField( max_length=30 ,required=False,help_text='Optional')
    last_name=forms.CharField( max_length=30, required=False,help_text='Optional')
    email=forms.EmailField(max_length=300, help_text="Enter the valid Email Adress")
    
    class Meta:
        model=User
        fields=('username','first_name','last_name','email','password1','password2',)

class CommentForm(forms.ModelForm):
     class Meta:
         models=Comments
         fields=('body',)

class ProfileEdit(forms.ModelForm):
    class Meta:
        models=UserChangeForm
        fields=('username','email',)