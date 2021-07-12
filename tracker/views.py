from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
# Create your views here.
from tracker.models import Milestone, Task, Workflow, Node, Line
from main.models import Client, Campaign
from datetime import datetime, timedelta
import json

def overview(request):
    if request.method == 'GET':
        context = {
            'clients': Client.objects.all(), #oder filter alle, die noch nicht fertig sind? (falls das je geht),
            'active_tasks': Task.objects.filter(
                due_date__lte=(datetime.now() + timedelta(days=2)),
                completion_date__isnull=True).order_by("due_date"),
            'campaigns': Campaign.objects.all()
        }
        return render(request, 'tracker/overview.html', context)
    else:
        if request.POST['action'] == 'REDIRECT':
            destination = request.POST['destination']
            if destination == 'WORKFLOW':
                return redirect('tracker:workflow', campaign_id=int(request.POST['campaign_id']))
            elif destination == 'CAMPAIGN':
                return redirect('main:edit_campaign', campaign_id=int(request.POST['campaign_id']))
        elif request.POST['action'] == 'NEW_CAMPAIGN':
            client = Client.objects.get(id=int(request.POST['client_id']))
            return redirect('main:new_campaign', client_id=client.id)
        return redirect('tracker:overview')

def workflow(request, campaign_id):
    campaign = Campaign.objects.get(id=campaign_id)
    if request.method == 'POST':
        if request.POST['action'] == 'START_WORKFLOW':
            campaign.workflow.start()
            return redirect('tracker:workflow', campaign_id=campaign_id)
        elif request.POST['action'] == 'FINISH_TASK':
            campaign.workflow.next_task(int(request.POST['task_id']))
            return redirect('tracker:workflow', campaign_id=campaign_id)
    client = campaign.client

    context = {
        'client': client,
        'campaign': campaign,
        'workflow': campaign.workflow,
        'start_date': campaign.workflow.first_date.timestamp() * 1000,
        'milestones': Milestone.objects.all(),
        'active_tasks': campaign.workflow.active_tasks()
    }
    return render(request, 'tracker/workflow.html', context)

def design_workflow(request, campaign_id):
    campaign = Campaign.objects.get(id=campaign_id)
    workflow = campaign.workflow

    if request.method == 'GET':
        context = {
            'campaign': campaign,
            'milestones': Milestone.objects.all(),
            'workflow': workflow
        }
        return render(request, 'tracker/design_workflow.html', context)

    data = json.loads(request.POST['data'])
    print(data)
    lines = []
    nodes = {}
    present_tasks = {task.id:task for task in workflow.task_set.all()}
    present_lines = workflow.get_lines()
    for obj in data['nodes']:
        print(obj)
        node = None
        if obj['id'] is not None:
            try:
                node = present_tasks[obj['id']].node
                del present_tasks[obj['id']]
            except KeyError:
                pass
            print(node)
        if node is None:
            node = Node()
            milestone = None
            try:
                milestone = Milestone.objects.get(id=obj['milestone_id'])
            except Milestone.DoesNotExist:
                pass
            t = Task(
                workflow = workflow,
                milestone = milestone,
                planned_start_date=datetime.now() #FALSCH ABER EGAL
            )
            t.save()
            node.task = t

        node.left = obj['left']
        node.top = obj['top']
        nodes[obj['nr']] = node

        node.save()

    for obj in data['lines']:
        if obj['id'] is not None:
            try:
                line = present_lines[obj['id']];
                del present_lines[obj['id']]
            except KeyError:
                line = Line()
        else:
            line = Line()
        line.from_node = nodes[obj['from']]
        line.to_node = nodes[obj['to']]
        line.save()

    for task in present_tasks.items():
        task[1].delete()
    for line in present_lines.items():
        line[1].delete()

    return redirect('tracker:design_workflow', campaign_id=campaign_id)


def list_milestones(request):
    return HttpResponse("Milestones")

def edit_milestone(request, milestone_pk):
    milestone = Milestone.objects.get(pk=milestone_pk)
    return HttpResponse("Edit Milestone")


#sollte man beide löschen können :(
#JAVASCRIPT BACKGROUND REQUESTS
def update_tasks(request, workflow_id):
    if request.method != 'POST':
        return HTTPResponse("Nope")

    workflow = Workflow.objects.get(id=workflow_id)

    data = json.loads(request.POST['tasks'])

    new_tasks = []
    for raw_task in data:
        try:
            task = Task.objects.get(id=raw_task['task_id'])
        except Task.DoesNotExist:
            task = Task(
                workflow = workflow,
                milestone = Milestone.objects.get(id=raw_task['milestone_id'])
            )
            new_tasks.append({'refnr': raw_task['refnr'], 'task': task})
        task.planned_start_date = datetime.fromtimestamp(raw_task['millis']['start'] / 1000)
        task.due_date = datetime.fromtimestamp(raw_task['millis']['end'] / 1000)
        task.save()

    new_tasks = [{'refnr': t['refnr'], 'task_id': t['task'].id} for t in new_tasks]
    return JsonResponse({'new_tasks': new_tasks});

def update_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except:
        return HttpResponse(status=404)

    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        pass
    if request.method == 'DELETE':
        task.delete()
        return HttpResponse(status=200)
    #return HttpResponse("NO")
