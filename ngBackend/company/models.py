from django.db import models
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    logo = models.ImageField(upload_to="static/companies/", default='static/companies/default.svg')
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    group = models.ForeignKey(Group, to_field="name", on_delete=models.CASCADE, related_name='companies')
    members = models.ManyToManyField(User, related_name='company_members')
    owner = models.ForeignKey(User, to_field="username", on_delete=models.CASCADE, related_name='company_owner', null=False)
