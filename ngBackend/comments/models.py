from django.db import models
from django.contrib.auth.models import User
from datetime import date
from announcements.models import Announcement
# Create your models here.

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment")
    announcement = models.ForeignKey(Announcement, related_name="announcements_comment", on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    content = models.TextField()