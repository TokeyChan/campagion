from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class Department(models.Model):
    name = models.CharField(max_length=40)
    color = models.CharField(max_length=10, default="#717171")

    def __str__(self):
        return self.name

class PermissionGroup(models.Model):
    name = models.CharField(max_length=80)
    codename = models.CharField(max_length=40)
    