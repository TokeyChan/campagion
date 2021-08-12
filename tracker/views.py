from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.urls import reverse
from django.db.models import Q
# Create your views here.
from tracker.models import Milestone, Task, Workflow, Node, Line, Template, Completer
from tracker.contrib.utils import handle_node_data
from tracker.forms import TemplateForm, UploadForm, MilestoneForm
from main.models import Client, Campaign
from users.models import Department
from datetime import datetime, timedelta
import json

def overview(request):
    if request.method == 'GET':
        context = {
            #'clients': Client.objects.all(), #oder filter alle, die noch nicht fertig sind? (falls das je geht),
            'active_tasks': Task.objects.active_tasks(),
            'campaigns': Campaign.objects.all().order_by('status')
        }
        return render(request, 'tracker/overview.html', context)
    else:
        if request.POST['action'] == 'REDIRECT':
            destination = request.POST['destination']
            if destination == 'WORKFLOW':
                return redirect('tracker:workflow', campaign_id=int(request.POST['campaign_id']))
            elif destination == 'EDIT_CAMPAIGN':
                return redirect('main:edit_campaign', campaign_id=int(request.POST['campaign_id']))
            elif destination == 'NEW_CAMPAIGN':
                return redirect('main:new_campaign')
        elif request.POST['action'] == 'FINISH_TASK':
            task = Task.objects.get(id=int(request.POST['task_id']))
            class_ = task.milestone.completer.handler_class()
            completer = class_(task, reverse('tracker:workflow', kwargs={'campaign_id': task.workflow.campaign.id}))
            return completer.handle()
        return redirect('tracker:overview')

def workflow(request, campaign_id):
    campaign = Campaign.objects.get(id=campaign_id)
    if request.method == 'POST':
        if request.POST['action'] == 'START_WORKFLOW':
            campaign.workflow.start(request)
            return redirect('tracker:workflow', campaign_id=campaign_id)
        elif request.POST['action'] == 'FINISH_TASK':
            task = Task.objects.get(id = int(request.POST['task_id']))
            if request.user != task.assigned_user():
                return HttpResponseForbidden()
            class_ = task.milestone.completer.handler_class()
            completer = class_(request, task, reverse('tracker:workflow', kwargs={'campaign_id': campaign_id}))
            return completer.handle()
        elif request.POST['action'] == 'RESET_TASK':
            task = Task.objects.get(id=int(request.POST['task_id']))
            if request.user != task.assigned_user():
                return HttpResponseForbidden()
            campaign.workflow.add_fallback_task(task)
            return
            return redirect('tracker:workflow', campaign_id=campaign_id)
        elif request.POST['action'] == 'OPEN_DESIGN':
            return redirect('tracker:design_workflow', campaign_id=campaign_id)
        elif request.POST['action'] == 'CHOOSE_TEMPLATE':
            return redirect('tracker:choose_template', campaign_id=campaign_id)
        elif request.POST['action'] == 'EDIT_CAMPAIGN':
            return redirect('main:edit_campaign', campaign_id=campaign_id)
    client = campaign.client
    workflow = campaign.workflow
    workflow.calculate_tasks()
    start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) if not workflow.is_started() else workflow.start_date.replace(hour=0, minute=0, second=0, microsecond=0)
    context = {
        'client': client,
        'campaign': campaign,
        'workflow': campaign.workflow,
        'start_date': start_date.timestamp() * 1000,
        'end_date': workflow.last_relevant_date().timestamp() * 1000,
        'active_tasks': campaign.workflow.active_tasks(),
        'departments': json.dumps([{'id': d.id, 'name': d.name + " (" + d.get_assignee_name(campaign) + ")"} for d in Department.objects.all()])
    }
    return render(request, 'tracker/workflow.html', context)

def design_workflow(request, campaign_id):
    campaign = Campaign.objects.get(id=campaign_id)
    workflow = campaign.workflow

    if request.method == 'GET':
        context = {
            'campaign': campaign,
            'milestones': Milestone.objects.filter(Q(campaign__isnull=True) | Q(campaign=campaign)),
            'workflow': workflow,
            'form': MilestoneForm(),
            'completers': Completer.objects.all()
        }
        return render(request, 'tracker/design_workflow.html', context)

    handle_node_data(request.POST['data'], workflow)

    return redirect('tracker:workflow', campaign_id=campaign_id)

# TEMPLATES
def choose_template(request, campaign_id):
    if request.method == 'GET':
        return render(request, 'tracker/choose_template.html', {
            'campaign_id': campaign_id,
            'templates': Template.objects.all()
        })

    if request.POST['action'] == 'CHOSEN':
        campaign = Campaign.objects.get(id=campaign_id)
        workflow = campaign.workflow
        workflow.copy_nodes(Template.objects.get(id=request.POST['template_id']))
        return redirect('tracker:workflow', campaign_id=campaign_id)
    elif request.POST['action'] == 'EDIT':
        return redirect('tracker:edit_template', template_id=int(request.POST['template_id']), campaign_id=campaign_id)
    elif request.POST['action'] == 'DELETE':
        t = Template.objects.get(id=int(request.POST['template_id']))
        t.delete()
        return redirect('tracker:choose_template', campaign_id=campaign_id)
    elif request.POST['action'] == 'NEW_TEMPLATE':
        return redirect('tracker:new_template', campaign_id=campaign_id)
    elif request.POST['action'] == 'ABORT':
        return redirect('tracker:workflow', campaign_id=campaign_id)

def edit_template(request, template_id, campaign_id):
    template = Template.objects.get(id=template_id)
    if request.method == 'GET':
        context = {
            'template': template,
            'milestones': Milestone.objects.all(),
            'use_template': True,
            'form': MilestoneForm(global_=True),
            'campaign_id': campaign_id
        }
        return render(request, 'tracker/design_workflow.html', context)

    handle_node_data(request.POST['data'], template)

    return redirect('tracker:choose_template', campaign_id=campaign_id) # Hier irgendwie zum Choose Template zurück

def new_template(request, campaign_id):
    if request.method == 'POST':
        form = TemplateForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('tracker:edit_template', template_id=form.instance.id, campaign_id=campaign_id)
    else:
        form = TemplateForm()
    context = {
        'class_name': 'Vorlage',
        'form': form,
        'new': True,
        'url': reverse('tracker:new_template', kwargs={'campaign_id': campaign_id})
    }
    return render(request, 'main/simple_form.html', context)
# END TEMPLATES

def list_milestones(request):
    return HttpResponse("Milestones")

def edit_milestone(request, milestone_pk):
    milestone = Milestone.objects.get(pk=milestone_pk)
    return HttpResponse("Edit Milestone")

def upload_file(request, task_id):
    task = Task.objects.get(id=task_id)
    if task.milestone.completer.name != "UploadCompleter":
        raise TypeError("Task hat keinen UploadCompleter")
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            form.save()
            class_ = task.milestone.completer.handler_class()
            completer = class_(request, task, None)
            completer.complete()
            return redirect('tracker:workflow', campaign_id=task.workflow.campaign.id)
    else:
        form = UploadForm(instance=task)
    return render(request, 'main/simple_form.html', {
        'class_name': task.milestone.upload_name + " hochladen",
        'form': form,
        'new': True,
        'url': reverse('tracker:upload_file', kwargs={'task_id': task_id}),
        'with_uploads': True
    })


#BACKGROUND
def bg_new_milestone(request, campaign_id):
    if request.method == "GET":
        raise ValueError("This view should never be accessed via GET")
    form = MilestoneForm(campaign_id == 0, request.POST)
    if form.is_valid():
        form.save(campaign_id)
        return JsonResponse({"html": "", 'milestone': form.instance.to_html()})
    return JsonResponse({
        'html': form.as_table(),
        'milestone': {}
    })