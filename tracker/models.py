from django.db import models
from main.models import Client, Campaign
from users.models import Department
import json
from datetime import datetime, timedelta
from importlib import import_module
from tracker.mails import send_task_mail
# Create your models here.

class Completer(models.Model):
    name = models.CharField(max_length=50) #bezeichnung des Completers
    handler = models.CharField(max_length=100) #Klasse, die die completion handelt
    explanation = models.CharField(max_length=50, blank=True)

    def handler_class(self):
        return getattr(self.module(), self.class_name())

    def module(self):
        path = self.handler.split('.')
        path.pop(-1)
        return import_module(".".join(path))
    
    def class_name(self):
        path = self.handler.split('.')
        return path[-1]

    def __str__(self):
        return self.explanation

def get_click_completer():
    return Completer.objects.get(name="ClickCompleter")

class Milestone(models.Model):
    name = models.CharField(max_length=150)
    duration = models.DurationField(default=timedelta(days=1))
    is_external = models.BooleanField(default=False)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    completer = models.ForeignKey("Completer", on_delete=models.SET_DEFAULT, default=get_click_completer) # 1 ist der ClickCompleter
    upload_dir = models.CharField(max_length=25, null=True, blank=True, unique=True) # nur notwendig, wenn der UploadCompleter gewählt wurde
    upload_name = models.CharField(max_length=50, null=True, blank=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    def hours(self):
        days = self.duration.days
        seconds = self.duration.seconds
        hours = (seconds // 3600) + (days * 24)

        return hours
    
    def to_html(self):
        return f"""
            <div class='milestone noselect' data-milestone_id='{self.id}'>
                <div class='milestone_name'>
                    {self.name}
                </div>
                <div class='milestone_duration'>
                    {"Extern" if self.is_external else str(self.hours()) + "h"}
                </div>
                <div class='milestone_department'>
                    {self.department.name}
                </div>
                <span class='dot left'></span>
                <span class='dot right'></span>
            </div>
            """

def calc_planned_dates(task): #recursive!!!
    if len(task.parent_tasks()) == 0:
        task.planned_start_date = datetime.now()
        task.due_date = task.planned_start_date + task.milestone.duration
        task.save()
        return datetime.now()
    parent_end_dates = []
    for parent in task.parent_tasks():
        start_date = calc_planned_dates(parent)
        parent_end_dates.append(start_date + parent.milestone.duration)
    task.planned_start_date = max(parent_end_dates)
    task.due_date = task.planned_start_date + task.milestone.duration
    task.save()
    return task.planned_start_date

def calc_dates(task): #auch recursive, geht nur, wenn der Workflow aktiv ist
    parent_end_dates = []
    if task.is_active():
        active_for = datetime.now() - task.start_date
        planned_duration = task.milestone.duration
        return task.start_date + (planned_duration if planned_duration > active_for else active_for)
    elif task.is_finished():
        return task.completion_date
    
    for parent in task.parent_tasks():
        end_date = calc_dates(parent)
        parent_end_dates.append(end_date)
    task.planned_start_date = max(parent_end_dates)
    task.due_date = task.planned_start_date + task.milestone.duration
    task.save()
    return task.due_date

class Workflow(models.Model):
    campaign = models.OneToOneField(Campaign, on_delete=models.CASCADE)
    start_date = models.DateTimeField(null=True, blank=True)

    def start(self, request):
        self.calculate_tasks()
        first_tasks = [task for task in self.task_set.all() if task.node.outgoing_lines.all().count() == 0]
        first_task = self.task_set.order_by('planned_start_date')[0]
        first_task.start_date = first_task.planned_start_date
        first_task.save()
        self.start_date = datetime.now()
        self.save()
        send_task_mail(first_task)

    def complete_task(self, request, task):
        task.completion_date = datetime.now()
        task.save()

        children = task.child_tasks()

        for child in children:
            parents = child.parent_tasks()
            start_possible = True
            for parent in parents:
                if not parent.is_finished():
                    start_possible = False
                    break
            if start_possible:
                child.start()
                if request.user != child.assigned_user:
                    send_task_mail(child)
        

    def calculate_tasks(self):
        started = self.is_started()

        last_tasks = [task for task in self.task_set.all() if len(task.node.outgoing_lines.all()) == 0]
        for task in last_tasks:
            if started:
                calc_dates(task)
            else:
                calc_planned_dates(task)
            

    def to_json(self):
        return json.dumps({'id': self.id })

    def tasks_to_json(self):
        return json.dumps([task.to_json() for task in sorted(self.task_set.all(), key=lambda x: x.start_date if x.start_date is not None else x.planned_start_date)])

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

    def copy_nodes(self, template):
        self.task_set.all().delete()
        nodes = {}
        lines = []
        for task in template.task_set.all():
            node = task.node
            for line in node.outgoing_lines.all():
                lines.append(line)
            t = Task()
            t.workflow = self
            t.milestone = task.milestone
            t.planned_start_date = datetime.now()
            t.save()
            n = Node()
            n.task = t
            n.left = node.left
            n.top = node.top
            n.save()
            nodes[node.id] = n
        lines_to_create = []
        for line in lines:
            l = Line()
            l.from_node = nodes[line.from_node.id]
            l.to_node = nodes[line.to_node.id]
            l.save()

class Template(models.Model):
    name = models.CharField(max_length=100)

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

class TaskManager(models.Manager):
    def active_tasks(self):
        return self.filter(
            due_date__lte=(datetime.now() + timedelta(days=2)),
            completion_date__isnull=True,
            workflow__start_date__isnull=False,
            start_date__isnull=False,
            milestone__is_external=False
        ).order_by("due_date")

def get_upload_to(instance, filename):
    now = datetime.now()
    return "/".join([
        instance.milestone.upload_dir,
        str(now.year),
        str(now.month),
        str(now.day),
        filename
     ])

class Task(models.Model):
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE, null=True, blank=True)
    template = models.ForeignKey(Template, on_delete=models.CASCADE, null=True, blank=True)
    milestone = models.ForeignKey(Milestone, on_delete=models.CASCADE, null=True)
    planned_start_date = models.DateTimeField()
    start_date = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    completion_date = models.DateTimeField(null=True, blank=True)
    uploaded_file = models.FileField(null=True, blank=True, upload_to=get_upload_to)
    #completion_user = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = TaskManager()

    def __str__(self):
        return self.milestone.name
    
    def start(self):
        self.start_date = datetime.now()
        self.due_date = self.start_date + self.milestone.duration
        self.save()

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
                #'color': milestone.color,
                'duration': milestone.hours(),
                'is_external': milestone.is_external,
                'department': {
                    'id': department.id,
                    'name': department.name
                }
            },
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
        delta = self.due_date - datetime.now()
        days = delta.days
        hours = delta.seconds // 3600 + (days * 24)
        return f"Fällig in {hours} Stunden"

    def is_finished(self):
        return self.completion_date != None

    def child_nodes(self):
        return [line.to_node for line in self.node.outgoing_lines.all()]

    def child_tasks(self):
        return [node.task for node in self.child_nodes()]

    def parent_tasks(self):
        return [line.from_node.task for line in self.node.incoming_lines.all()]

    def assigned_user(self):
        return self.workflow.campaign.assignee_set.get(department=self.milestone.department).user

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
