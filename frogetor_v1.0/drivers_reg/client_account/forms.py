from django import forms
from .models import UserProfile

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    remember_me = forms.BooleanField(required=False)

class RegistrationForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password', 'mobile_number']
        
    confirm_password = forms.CharField(max_length=128, widget=forms.PasswordInput())