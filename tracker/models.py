from django.db import models

from main.models import Client, Campaign
# Create your models here.

class Milestone(models.Model):
    name = models.CharField(max_length=150)
    duration = models.DurationField()
    order = models.IntegerField()
    #color = models.ColorField() # musst du noch machen
    is_active = models.BooleanField()

class Task(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    milestone = models.ForeignKey(Milestone, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    due_date = models.DateTimeField()
