from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth import login as login_user
from django.contrib.auth import logout
from django.contrib import messages
from django.conf import settings
from django.views.decorators.clickjacking import xframe_options_sameorigin

from .models import Campaign, Client, User
from users.models import Department
from campagion.contrib.utils import ModuleManager
from tracker.models import Workflow
from main.forms import ClientForm
from .forms import CampaignForm, LoginForm, ClientForm, CampaignDataForm
from django.contrib import messages

from datetime import date, datetime, timedelta
# Create your views here.

def index(request):
    if request.method == 'GET':
        request.session['active_module'] = None
        module_manager = ModuleManager()
        context = {
            'modules': module_manager.get_modules(request, [
                'dashboard',
                'clients',
                'users',
                'commissions'
            ])
        }
        return render(request, 'main/index.html', context)
    else:
        if request.POST['action'] == 'REDIRECT':
            m = Module(request.POST['module'])
            request.session['active_module'] = request.POST['module']
            return redirect(m.home_view)

def new_campaign(request):
    if request.method == 'POST':
        form = CampaignForm(request.POST)
        if form.is_valid():
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
        'client_form': ClientForm(),
        'new': True
    }
    return render(request, 'main/edit_campaign.html', context)

def get_folder_name(path):
    elements = path.split('/')
    index = elements.index(settings.MEDIA_ROOT.replace('/', ''))
    return elements[index + 1]
    
def edit_campaign(request, campaign_id):
    campaign = Campaign.objects.get(id=campaign_id)
    if request.method == 'POST':
        action = request.POST.get('action', None)
        if action == 'SAVE_CAMPAIGN':
            form = CampaignForm(request.POST, instance=campaign)

            if form.is_valid():
                form.save()
                return redirect('main:edit_campaign', campaign_id=campaign_id)
        elif action == 'START_CAMPAIGN':
            campaign.start_date = datetime.now()
            campaign.status = Campaign.Status.ACTIVE
            campaign.save()
            messages.success(request, "Die Kampagne wurde erfolgreich gestartet")
            return redirect('main:edit_campaign', campaign_id=campaign_id)
        elif action == 'END_CAMPAIGN':
            campaign.end_date = datetime.now()
            campaign.status = Campaign.Status.FINISHED
            campaign.save()
            messages.success(request, "Die Kampagne wurde erfolgreich beendet")
            return redirect('main:edit_campaign', campaign_id=campaign_id)
    else:
        form = CampaignForm(instance=campaign)

    files = campaign.get_files()

    folders = {}
    for file in files:
        folder_name = get_folder_name(file.path)
        if folder_name in folders:
            folders[folder_name].append(file)
        else:
            folders[folder_name] = [file]

    context = {
        'campaign': campaign,
        'form': form,
        'folders': folders,
        'client_form': ClientForm()
    }
    return render(request, 'main/edit_campaign.html', context)

def clients(request):
    clients = Client.objects.all()
    clients_with_campaigns = []
    clients_without_campaigns = []
    
    for client in clients:
        if len(client.relevant_campaigns()) != 0:
            clients_with_campaigns.append(client)
        else:
            clients_without_campaigns.append(client)
    

    context = {
        'clients': sorted(clients_with_campaigns, key=lambda x: x.name) + sorted(clients_without_campaigns, key=lambda x: x.name)
    }
    return render(request, 'main/clients.html', context)

def new_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:clients')
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
            return redirect('main:clients')
    else:
        form = ClientForm(instance=client)
    
    context = {
        'class_name': 'Kunde',
        'form': form,
        'new': False,
        'url': reverse('main:edit_client', kwargs={'client_id': client_id})
    }
    return render(request, 'main/simple_form.html', context)

def post_handler(request):
    if request.method == 'GET':
        raise TypeError("This View should never be accessed by a GET request")

    action = request.POST['action']
    if action == 'LOGOUT':
        logout(request)
        return redirect('users:login')
    if action == 'HOME':
        m = Module(request.session['active_module'])
        return redirect(m.home_view)
    if action == 'TO_INDEX':
        return redirect('main:index')


# BACKGROUND
def bg_new_client(request):
    if request.method == "GET":
        raise ValueError("This view should never be accessed via GET")
    form = ClientForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({"html": "", 'option': f"<option value='{form.instance.id}'>{form.instance.name}</option>"})
    return JsonResponse({
        'html': form.as_table(),
        'option': {}
    })