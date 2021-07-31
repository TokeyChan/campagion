from django.db import models
from dateutil.parser import parse
from decimal import Decimal
from datetime import datetime

class CampaignData(models.Model):
    api_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    campaign_type = models.CharField(max_length=50, null=True, blank=True)
    device_type = models.CharField(max_length=50, null=True, blank=True)
    target_group = models.CharField(max_length=50, null=True, blank=True)
    daily_budget = models.DecimalField(decimal_places=4, max_digits=10, null=True, blank=True)
    daily_budget_left = models.DecimalField(decimal_places=4, max_digits=10, null=True, blank=True)
    added_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=30, null=True, blank=True)
    number_of_bids = models.IntegerField(null=True, blank=True)
    paused_ads = models.IntegerField(null=True, blank=True)
    number_of_creatives = models.IntegerField(null=True, blank=True)
    number_of_time_targets = models.IntegerField(null=True, blank=True)
    stats = models.ForeignKey("CampaignStats", on_delete=models.CASCADE, null=True, blank=True)

    def create(self, data):
        self.api_id = data.get('campaign_id', None)
        self.name = data.get('campaign_name', None)
        self.campaign_type = data.get('campaign_type', None)
        self.device_type = data.get('campaign_device_type', None)
        self.target_group = data.get('campaign_target_group', None)
        self.daily_budget = Decimal(data.get('campaign_daily_budget', None))
        self.daily_budget_left = Decimal(data.get('daily_budget_left', None))
        self.added_date = parse(data.get('added_date', None)).replace(tzinfo=None)
        self.status = data.get('status', None)
        self.number_of_bids = int(data.get('number_of_bids', None))
        self.paused_ads = int(data.get('paused_ads', None))
        self.number_of_creatives = int(data.get('number_of_creatives', None))
        self.number_of_time_targets = int(data.get('number_of_time_targets', None))

class CampaignStats(models.Model):
    impressions = models.IntegerField(null=True, blank=True)
    iframes = models.IntegerField(null=True, blank=True)
    revenue = models.DecimalField(decimal_places=4, max_digits=15, null=True, blank=True)
    clicks = models.IntegerField(null=True, blank=True)
    ctr = models.DecimalField(decimal_places=4, max_digits=10, null=True, blank=True)
    ecpm = models.DecimalField(decimal_places=4, max_digits=10, null=True, blank=True)
    ecpc = models.DecimalField(decimal_places=4, max_digits=10, null=True, blank=True)
    conversions = models.IntegerField(null=True, blank=True)
    last_update = models.DateTimeField(null=True, blank=True)

    def update(self, data):
        if len(data) == 0:
            return
        self.impressions = int(data['impressions'])
        self.iframes = int(data['iframes'])
        self.revenue = data['revenue']
        self.clicks = int(data['clicks'])
        self.ctr = data['ctr']
        self.ecpm = data['ecpm']
        self.ecpc = data['ecpc']
        self.conversions = data['conversions']
        self.last_update = datetime.now()
