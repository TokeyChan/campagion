from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login as login_user
from django.contrib.auth import logout

from .models import Campaign, Client
from main.contrib.utils import Module
from tracker.models import Workflow
from .forms import CampaignForm, LoginForm, ClientForm

from datetime import datetime, timedelta
# Create your views here.

def main(request):
    if request.method == 'GET':
        context = {
            'modules': [
                Module('tracker'),
                Module('users')
            ]
        }
        return render(request, 'main/main.html', context)
    else:
        if request.POST['action'] == 'REDIRECT':
            return redirect(request.POST['destination'])

def users(request):
    pass

def new_campaign(request, client_id):
    client = Client.objects.get(id=client_id)
    if request.method == 'POST':
        form = CampaignForm(request.POST)

        if form.is_valid():
            form.instance.client = client
            form.save()
            w = Workflow(campaign=form.instance)
            w.first_date = datetime.now() - timedelta(days=1)
            w.save()
            return redirect('tracker:choose_template', campaign_id=form.instance.id)
    else:
        form = CampaignForm()
    context = {
        'class_name': 'Kampagne',
        'form': form,
        'new': True,
        'url': reverse('main:new_campaign', kwargs={'client_id': client_id})
    }
    return render(request, 'main/simple_form.html', context)

def edit_campaign(request, campaign_id):
    campaign = Campaign.objects.get(id=campaign_id)
    if request.method == 'POST':
        form = CampaignForm(request.POST, instance=campaign)

        if form.is_valid():
            form.save()
            return redirect('tracker:overview')
    else:
        form = CampaignForm(instance=campaign)

    context = {
        'class_name': "Kampagne",
        'form': form,
        'new': False,
        'url': reverse('main:edit_campaign', kwargs={'campaign_id': campaign_id})
    }
    return render(request, 'main/simple_form.html', context)

def new_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tracker:overview')
    else:
        form = ClientForm()

    context = {
        'class_name': "Kunde",
        'form': form,
        'new': True,
        'url': reverse('main:new_client')
    }
    return render(request, 'main/simple_form.html', context)

def edit_client(request, client_id):
    client = Client.objects.get(id=client_id)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('tracker:overview')
    else:
        form = ClientForm()
    
    context = {
        'class_name': 'Kunde',
        'form': form,
        'new': False,
        'url': reverse('main:edit_client', kwargs={'client_id': client_id})
    }

def post_handler(request):
    if request.method == 'GET':
        raise TypeError("This View should never be accessed by a GET request")
    
    action = request.POST['action']
    if action == 'LOGOUT':
        logout(request)
        return redirect('users:login')
    if action == 'TO_OVERVIEW':
        return redirect('tracker:overview')
