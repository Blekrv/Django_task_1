from django.db import models
from django import forms
from .models import Posts


class PostForm(forms.ModelForm):

    class Meta:
        model = Posts
        fields = ('title', 'text')


class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email_address = forms.EmailField(max_length=50)
    message = forms.CharField(widget=forms.Textarea, max_length=2000)


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
