from django.db import models
from django.urls import reverse
from django.conf import settings
from main.models import Assignee
import uuid

# Create your models here.

class Department(models.Model):
    name = models.CharField(max_length=40)
    color = models.CharField(max_length=10, default="#717171")

    def __str__(self):
        return self.name

    def get_assignee_name(self, campaign):
        try:
            return Assignee.objects.get(department=self, campaign=campaign).user.name()
        except Assignee.DoesNotExist:
            return None

class PermissionGroup(models.Model):
    name = models.CharField(max_length=80)
    codename = models.CharField(max_length=40)

    def __str__(self):
        return self.name
    
class Invitation(models.Model):
    invitor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="invitations")
    email = models.EmailField()
    key = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    group = models.ForeignKey(PermissionGroup, on_delete=models.SET_NULL, null=True)
    
    def link(self):
        return settings.HOST_NAME + reverse('users:register', kwargs={'key': self.key})