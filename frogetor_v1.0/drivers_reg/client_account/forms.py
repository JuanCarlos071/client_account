from django import forms
from .models import UserProfile
from django.contrib.auth.hashers import make_password  # Import make_password


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    remember_me = forms.BooleanField(required=False)

# class RegistrationForm(forms.ModelForm):

#     class Meta:
#         model = UserProfile
#         fields = ['username', 'email', 'password', 'mobile_number']
        
#     confirm_password = forms.CharField(max_length=128, widget=forms.PasswordInput())
    
class RegistrationForm(forms.ModelForm):
    password = forms.CharField(max_length=128, widget=forms.PasswordInput())
    confirm_password = forms.CharField(max_length=128, widget=forms.PasswordInput())

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password', 'mobile_number']

    def save(self, commit=True):
        # Override the save method to hash the password before saving
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data['password'])  # Hash the password
        if commit:
            user.save()
        return user