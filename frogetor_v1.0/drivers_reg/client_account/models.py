from django.db import models
from django.contrib.auth.models import User
import hashlib
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

    def check_password(self, plain_password):
        # Hash the plain-text password using the same algorithm used during registration
        hashed_password = hashlib.sha256(plain_password.encode()).hexdigest()
        # Compare the hashed password with the stored hashed password
        return hashed_password == self.password, hashed_password
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'