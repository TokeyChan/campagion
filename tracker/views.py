from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from tracker.models import Milestone
from main.models import Client

def overview(request):
    clients = Client.objects.all() #oder filter alle, die noch nicht fertig sind? (falls das je geht)
    return render(request, 'tracker/overview.html', {'clients': clients})

def details(request, client_pk):
    client = Client.objects.get(pk=client_pk)
    return HttpResponse("Details")

def list_milestones(request):
    return HttpResponse("Milestones")

def edit_milestone(request, milestone_pk):
    milestone = Milestone.objects.get(pk=milestone_pk)
    return HttpResponse("Edit Milestone")
