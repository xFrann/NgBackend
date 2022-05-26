from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=80, default='')
    last_name = models.CharField(max_length=80, default='')
    phone = models.CharField(max_length=20, default='')
    picture = models.ImageField(upload_to="static/", default='static/profile.jpg')

    def __str__(self):
        return self.first_name

        # REMOVE CITY AS IT'S USELESS