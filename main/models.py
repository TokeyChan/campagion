from django.db import models
from django.db.models import Q, Sum
from datetime import datetime, date, timedelta
from django.contrib.auth.models import AbstractUser, UserManager
from functools import cached_property
from decimal import Decimal
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
    group = models.ForeignKey("users.PermissionGroup", on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)


    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.name()

    def name(self):
        return self.first_name + " " + self.last_name

    @cached_property
    def is_admin(self):
        return self.group.codename == "ADMIN"
    

class Client(models.Model):
    name = models.CharField(max_length=90)
    contact_name = models.CharField(max_length=90, null=True, blank=True)
    phone = models.CharField(max_length=40, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    #is_visible = models.BooleanField(default=True)

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

def get_planned_start_date():
    return datetime.now() + timedelta(days=21)

class Campaign(models.Model):
    class Status(models.IntegerChoices):
        ACTIVE = 1
        PRE_ACTIVE = 2
        FINISHED = 3

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    planned_start_date = models.DateField(null=True, blank=True, default=get_planned_start_date)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    budget = models.DecimalField(decimal_places=2, max_digits=10)
    campagion_budget = models.DecimalField(decimal_places=2, max_digits=10)
    days = models.IntegerField()
    status = models.IntegerField(choices=Status.choices, default=Status.PRE_ACTIVE)
    commission = models.ForeignKey("administration.Commission", on_delete=models.SET_NULL, null=True, blank=True)
    fee_percentage = models.IntegerField(default=15)

    def __str__(self):
        return self.name

    def is_started(self):
        return self.start_date is not None

    def has_ended(self):
        return self.end_date is not None

    def runtime_string(self):
        start, end, is_plan = None, None, True

        if self.start_date == None and self.planned_start_date == None:
            return "Zeitraum noch unklar"
        elif self.start_date == None: #wenn es noch nicht gestartet ist, aber es einen planm????igen Start gibt
            start, end = self.planned_start_date, (self.planned_start_date + timedelta(days=self.days))
        else:
            start = self.start_date
            end = self.end_date if self.end_date is not None else (self.start_date + timedelta(days=self.days))
            is_plan = False

        return start.strftime("%d.%m.%Y") + " - " + end.strftime("%d.%m.%Y")

    def is_relevant(self):
        return self.status == Campaign.Status.ACTIVE or self.status == Campaign.Status.PRE_ACTIVE

    def is_active(self):
        return self.status == Campaign.Status.ACTIVE
    def is_pre_active(self):
        return self.status == Campaign.Status.PRE_ACTIVE
    def is_finished(self):
        return self.status == Campaign.Status.FINISHED

    def status_color(self):
        if self.status == Campaign.Status.PRE_ACTIVE:
            return "#ffa200"
        elif self.status == Campaign.Status.ACTIVE:
            return "#63de2f"
        else:
            return "#bababa"

    def date_string(self):
        if self.status == Campaign.Status.PRE_ACTIVE:
            return "Start geplant am " + self.planned_start_date.strftime("%d.%m.%Y")
        elif self.status == Campaign.Status.ACTIVE:
            return self.start_date.strftime("%d.%m.%Y") + " - " + (self.start_date + timedelta(days=self.days)).strftime("%d.%m.%Y")
        else:
            return "Geendet am " + self.end_date.strftime("%d.%m.%Y")

    def expenses(self):
        expenses = Decimal(0)
        for child in self.children_set.all():
            expenses += child.stats_set.all().aggregate(Sum('revenue'))['revenue__sum']
        return expenses


    def budget_left(self):
        return self.budget - self.expenses()

    def get_files(self):
        tasks_with_files = self.workflow.task_set.exclude(Q(uploaded_file='') | Q(uploaded_file=None))
        return [task.uploaded_file for task in tasks_with_files]

    def commission_amount(self):
        return round((Decimal(0.035) * self.budget) + (Decimal(0.1) * self.campagion_budget), 2)

    def planned_end_date(self):
        if self.start_date is None:
            return None
        return self.start_date + timedelta(days=self.days)

class MiniCampaign(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='children_set')
    name = models.CharField(max_length=50)
    api_id = models.IntegerField(null=True, blank=True)

    def get_stats(self, stats = None):
        if stats is None:
            stats = self.stats_set.all()
        return stats.aggregate(
                    impressions=Sum('impressions'), 
                    revenue=Sum('revenue'), 
                    clicks=Sum('clicks'),
                    conversions=Sum('conversions')
                )

class Assignee(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.ForeignKey("users.Department", on_delete=models.CASCADE)

    def __str__(self):
        return self.user.name() + " - " + self.department.name