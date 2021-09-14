from django.contrib import admin
from main.models import Client, Campaign, User, Assignee, MiniCampaign
from main.api_models import CampaignStats

# Register your models here.
admin.site.register(User)
admin.site.register(Client)
admin.site.register(Campaign)
admin.site.register(Assignee)
admin.site.register(CampaignStats)
admin.site.register(MiniCampaign)
