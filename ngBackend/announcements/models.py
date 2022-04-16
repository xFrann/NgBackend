from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Announcement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="annoucements")