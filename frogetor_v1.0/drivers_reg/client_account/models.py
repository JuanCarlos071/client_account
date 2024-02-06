from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class LoginHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_timestamp = models.DateTimeField(auto_now_add=True)
    remember_me = models.BooleanField(default=False)


class UserProfile(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
