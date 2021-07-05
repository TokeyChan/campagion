from django.shortcuts import render, redirect

from .models import Campaign, Client
from tracker.models import Workflow
from .forms import CampaignForm

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
            w.create_tasks()
            return redirect('tracker:workflow', campaign_id=form.instance.id)
    else:
        form = CampaignForm()
    context = {
        'form': form,
        'new': True,
        'client': client
    }
    return render(request, 'main/campaign.html', context)

def edit_campaign(request, campaign_id):
    campaign = Campaign.objects.get(id=campaign_id)
    pass
