from django.db import models

from main.models import Client, Campaign, Department
import json
from datetime import datetime, timedelta
# Create your models here.
class Completer(models.Model):
    name = models.CharField(max_length=50) #bezeichnung des Completers
    handler = models.CharField(max_length=100) #Klasse, die die completion handelt

    def __str__(self):
        return self.name

class Milestone(models.Model):
    name = models.CharField(max_length=150)
    duration = models.DurationField()
    is_external = models.BooleanField(default=False)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    completer = models.ForeignKey("Completer", on_delete=models.SET_DEFAULT, default=1) # 1 ist der ClickCompleter

    def __str__(self):
        return self.name

    def hours(self):
        days = self.duration.days
        seconds = self.duration.seconds
        hours = (seconds // 3600) + (days * 24);

        return hours;


def calc_planned_start_date(task): #recursive!!!
    if len(task.parent_tasks()) == 0:
        task.planned_start_date = datetime.now()
        task.due_date = task.planned_start_date + task.milestone.duration
        task.save()
        return datetime.now()
    parent_end_dates = []
    for parent in task.parent_tasks():
        start_date = calc_planned_start_date(parent)
        parent_end_dates.append(start_date + parent.milestone.duration)
    task.planned_start_date = max(parent_end_dates)
    task.due_date = task.planned_start_date + task.milestone.duration
    task.save()
    return task.planned_start_date


class Workflow(models.Model):
    campaign = models.OneToOneField(Campaign, on_delete=models.CASCADE)
    start_date = models.DateTimeField(null=True, blank=True)

    def start(self):
        self.calculate_tasks()
        first_task = self.task_set.order_by('planned_start_date')[0]
        first_task.start_date = first_task.planned_start_date
        first_task.save()
        self.start_date = datetime.now()
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

    def calculate_tasks(self):
        print(self.is_started())
        if self.is_started():
            pass
        else:
            last_tasks = [task for task in self.task_set.all() if len(task.node.outgoing_lines.all()) == 0]
            for task in last_tasks:
                calc_planned_start_date(task)

    def to_json(self):
        return json.dumps({'id': self.id })

    def tasks_to_json(self):
        return json.dumps([task.to_json() for task in sorted(self.task_set.all(), key=lambda x: x.start_date if x.start_date is not None else x.planned_start_date)]);

    def is_finished(self):
        return all(task.is_finished() for task in self.task_set.all()) and self.is_started()

    def active_tasks(self):
        return [task for task in self.task_set.all() if task.is_active()]

    def get_nodes(self):
        obj = {'tasks': [], 'lines': []}
        for task in self.task_set.all():
            if task.node == None:
                continue #Das geht in Zukunft gar nicht
            obj['tasks'].append(task.to_json(with_node=True))
            for line in task.node.outgoing_lines.all():
                obj['lines'].append({'id': line.id, 'from': line.from_node.task.id, 'to': line.to_node.task.id})
        return json.dumps(obj)

    def get_lines(self):
        lines = []
        for task in self.task_set.all():
            lines.extend(task.node.outgoing_lines.all())
        return {line.id:line for line in lines}

    def is_started(self):
        return self.start_date != None

    def last_relevant_date(self):
        try:
            return self.task_set.order_by("-due_date")[0].due_date + timedelta(days=1)
        except IndexError:
            return datetime.now() + timedelta(days=20)

class Template(models.Model):
    name = models.CharField(max_length=100)

class Task(models.Model):
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)
    template = models.ForeignKey(Template, on_delete=models.CASCADE, null=True, blank=True)
    milestone = models.ForeignKey(Milestone, on_delete=models.CASCADE, null=True)
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

    def to_json(self, with_node = False):
        milestone = self.milestone
        department = self.milestone.department
        result = {
            'id': self.id,
            'milestone': {
                'name': milestone.name,
                'id': milestone.id,
                'color': milestone.color,
                'duration': milestone.hours(),
                'department': {
                    'id': department.id,
                    'name': department.name
                }
            },
            'is_external': milestone.is_external,
            'planned_start_date': self.planned_start_date.timestamp() * 1000 if self.planned_start_date != None else None,
            'start_date': self.start_date.timestamp() * 1000 if self.start_date != None else None,
            'due_date': self.due_date.timestamp() * 1000 if self.due_date != None else None,
            'completion_date': self.completion_date.timestamp() * 1000 if self.completion_date != None else None,
        }
        if with_node:
            node = {
                'id': self.node.id,
                'left': self.node.left,
                'top': self.node.top
            }
            result['node'] = node
        return result

    def date_string(self): # WAS, WENN ES NICHT ACTIVE IST?
        if self.milestone.is_external:
            return "Extern"
        return self.start_date.strftime("%d.%m.%Y %H:%M") + " - " + self.due_date.strftime("%d.%m.%Y %H:%M")

    def is_finished(self):
        return self.completion_date != None

    def child_nodes(self):
        return [line.to_node for line in self.node.outgoing_lines.all()]

    def parent_tasks(self):
        return [line.from_node.task for line in self.node.incoming_lines.all()]

class Node(models.Model):
    task = models.OneToOneField(Task, on_delete=models.CASCADE)
    left = models.IntegerField()
    top = models.IntegerField()

class Line(models.Model):
    from_node = models.ForeignKey(Node, on_delete=models.CASCADE, related_name="outgoing_lines")
    to_node = models.ForeignKey(Node, on_delete=models.CASCADE, related_name="incoming_lines")

#class ControlPoint(models.Model):
#   line = models.ForeignKey(Line, on_delete=models.CASCADE)
#   x = models.IntegerField()
#   y = models.IntegerField();
