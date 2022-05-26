from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class InviteCode(models.Model):
    code = models.CharField(max_length=10)
    used = models.BooleanField(default=False)
    used_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code