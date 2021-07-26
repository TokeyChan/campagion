from django.db import models
from datetime import datetime, date, timedelta
from django.contrib.auth.models import AbstractUser, UserManager
from users.models import PermissionGroup
# Create your models here.

class CustomUserManager(UserManager):
    def selection_source(self):
        options = []
        users = User.objects.all()
        options = [f"<option value='{user.id}'>{user.name()}</option>" for user in users]
        return "\n".join(options)

class User(AbstractUser):
    profile_picture = models.ImageField(upload_to="profile_pictures/%y/%m/%d/", null=True, blank=True)
    email = models.EmailField(unique=True)
    groups = None
    group = models.ForeignKey(PermissionGroup, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)


    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name()
    def name(self):
        return self.first_name + " " + self.last_name

class Client(models.Model):
    name = models.CharField(max_length=90)
    contact_name = models.CharField(max_length=90, null=True, blank=True)
    phone = models.CharField(max_length=40, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

    def current_tasks(self):
        return [task for task in self.tasks() if task.is_active()]

    def tasks(self):
        tasks = []
        for campaign in self.campaign_set.all():
            tasks += campaign.workflow.task_set.all()
        return tasks

    def relevant_campaigns(self):
        return [campaign for campaign in self.campaign_set.all() if campaign.is_relevant()]

def get_upload_to(campaign, filename):
    return f"contracts/{campaign.client.id}/{filename}"

def default_end_date():
    return datetime.now() + timedelta(days=21)

class Campaign(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    desc = models.CharField(max_length=100)
    contract = models.FileField(upload_to=get_upload_to, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True, default=datetime.now)
    end_date = models.DateField(null=True, blank=True, default=default_end_date)
    daily_budget = models.IntegerField()

    def runtime_string(self):
        if self.start_date == None or self.end_date == None:
            return "Zeitraum noch unklar"
        return self.start_date.strftime("%d.%m.%Y") + " - " + self.end_date.strftime("%d.%m.%Y")

    def is_relevant(self):
        return (self.end_date > datetime.now().date()) if self.end_date != None else True

    def is_active(self):
        return (self.start_date < datetime.now().date() and self.end_date > datetime.now().date()) if (self.end_date != None and self.start_date != None) else True

    def status(self, html=True):
        wf = self.workflow
        if not wf.is_started(): #wartet auf workflow
            return "Workflow noch nicht gestartet"
        elif wf.is_finished(): #alles abgeschlossen
            if self.is_active():
                return "Laufend - Nächstes Reporting in ###"
            else:
                return "Beginnt am " + self.start_date.strftime("%d.%m.%Y")
        else: #workflow ist aktiv
            newline = "<br>" if html else "\n"
            return (newline + newline).join([task.milestone.name + newline + task.due_date_string() for task in self.workflow.active_tasks()])

class Assignee(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.ForeignKey("users.Department", on_delete=models.CASCADE)

    def __str__(self):
        return self.user.name() + " - " + self.department.name