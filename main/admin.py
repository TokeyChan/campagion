from django.contrib import admin
from main.models import Client, Campaign, User, Assignee
from main.api_models import CampaignStats, CampaignData

# Register your models here.
admin.site.register(User)
admin.site.register(Client)
admin.site.register(Campaign)
admin.site.register(Assignee)
admin.site.register(CampaignData)
admin.site.register(CampaignStats)
