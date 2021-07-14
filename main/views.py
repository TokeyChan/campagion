from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login as login_user
from django.contrib.auth import logout

from .models import Campaign, Client
from tracker.models import Workflow
from .forms import CampaignForm, LoginForm

from datetime import datetime, timedelta
# Create your views here.

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
        'class_name': "Vorlage",
        'form': form,
        'new': False,
        'url': reverse('main:edit_campaign', kwargs={'campaign_id': campaign_id})
    }
    return render(request, 'main/simple_form.html', context)

def new_client(request):
    pass

def edit_client(request):
    pass

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.authenticate(request)
            if user is not None:
                login_user(request, user)
                return redirect('tracker:overview')
    else:
        form = LoginForm()
    context = {
        'form': form
    }
    return render(request, 'main/login.html', context)

def post_handler(request):
    if request.method == 'GET':
        raise TypeError("This View should never be accessed by a GET request")
    
    action = request.POST['action']
    if action == 'LOGOUT':
        logout(request)
        return redirect('main:login')
    if action == 'TO_OVERVIEW':
        return redirect('tracker:overview')
