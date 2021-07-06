from django.db import models

from main.models import Client, Campaign
import json
from datetime import datetime
# Create your models here.

class Milestone(models.Model):
    name = models.CharField(max_length=150)
    duration = models.DurationField()
    index = models.IntegerField()
    color = models.CharField(max_length=15) # Kannst du auch zu ColorField machen, wenn du ein ColorField machst
    is_external = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def hours(self):
        days = self.duration.days
        seconds = self.duration.seconds
        hours = (seconds // 3600) + (days * 24);

        return hours;

class Workflow(models.Model):
    campaign = models.OneToOneField(Campaign, on_delete=models.CASCADE)
    first_date = models.DateTimeField() #Also: Default-mäßig werden 2 Wochen angezeigt, aber kann sein, dass es länger dauert.
    started = models.BooleanField(default=False)

    def start(self):
        first_task = self.task_set.order_by('planned_start_date')[0]
        first_task.start_date = first_task.planned_start_date
        first_task.save()
        self.started = True
        self.save()

    def next_task(self, task_id):
        last_task = self.task_set.get(id=task_id)
        last_task.completion_date = datetime.now()
        last_task.save()
        due = last_task.due_date.replace(tzinfo=None) - last_task.completion_date

        tasks = self.task_set.order_by('planned_start_date')
        found = False
        for task in tasks:
            if not task.is_finished() and not found:
                found = True
                task.start_date = datetime.now()
            else:
                task.planned_start_date = task.planned_start_date + due
            task.save()

    def create_tasks(self):
        date = datetime.now()
        for milestone in Milestone.objects.order_by("index"):
            t = Task(
                workflow = self,
                milestone = milestone,
                planned_start_date = date,
                due_date = date + milestone.duration
            )
            t.save()
            date += milestone.duration

    def to_json(self):
        return json.dumps({'id': self.id })

    def tasks_to_json(self):
        return json.dumps([task.to_json() for task in sorted(self.task_set.all(), key=lambda x: x.start_date if x.start_date is not None else x.planned_start_date)]);

    def is_finished(self):
        return all(task.is_finished() for task in self.task_set.all()) and self.started

    def active_tasks(self):
        return [task for task in self.task_set.all() if task.is_active()]




class Task(models.Model):
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)
    milestone = models.ForeignKey(Milestone, on_delete=models.CASCADE)
    planned_start_date = models.DateTimeField()
    start_date = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    completion_date = models.DateTimeField(null=True, blank=True)
    #completion_user = models.ForeignKey(User, on_delete=models.CASCADE)

    def is_active(self):
        return self.start_date != None and self.completion_date == None

    def due_date_string(self): # Stattdessen sollte das sowas werden wie "Morgen um 9:00"
        if self.due_date == None:
            return ""
        if self.milestone.is_external:
            return "(Extern)"
        delta = self.due_date - datetime.now()
        days = delta.days
        hours = delta.seconds // 3600
        return f"{days} Tage und {hours} Stunden"

    def client(self):
        return self.workflow.campaign.client

    def to_json(self):
        milestone = self.milestone
        return {
            'id': self.id,
            'milestone': {
                'name': milestone.name,
                'id': milestone.id,
                'color': milestone.color
            },
            'is_external': milestone.is_external,
            'planned_start_date': self.planned_start_date.timestamp() * 1000 if self.planned_start_date != None else None,
            'start_date': self.start_date.timestamp() * 1000 if self.start_date != None else None,
            'due_date': self.due_date.timestamp() * 1000 if self.due_date != None else None,
            'completion_date': self.completion_date.timestamp() * 1000 if self.completion_date != None else None
        }

    def date_string(self): # WAS, WENN ES NICHT ACTIVE IST?
        if self.milestone.is_external:
            return "Extern"
        return self.start_date.strftime("%d.%m.%Y %H:%M") + " - " + self.due_date.strftime("%d.%m.%Y %H:%M")

    def is_finished(self):
        return self.completion_date != None
