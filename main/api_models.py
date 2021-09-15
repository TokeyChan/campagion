from django.db import models
from dateutil.parser import parse
from decimal import Decimal
from datetime import datetime
from .models import MiniCampaign

class CampaignStats(models.Model):
    minicampaign = models.ForeignKey(MiniCampaign, on_delete=models.CASCADE, related_name='stats_set', null=True)
    date = models.DateField()
    impressions = models.IntegerField(null=True, blank=True)
    iframes = models.IntegerField(null=True, blank=True)
    revenue = models.DecimalField(decimal_places=4, max_digits=15, null=True, blank=True)
    clicks = models.IntegerField(null=True, blank=True)
    conversions = models.IntegerField(null=True, blank=True)

    @property
    def ecpm(self):
        return (self.revenue / self.impressions) * 1000

    @property
    def ctr(self):
        return (self.clicks / self.impressions) * 100

    @property
    def cpc(self):
        return (self.revenue / self.clicks)

    def update(self, data):
        sum_ = {
            'impressions': 0,
            'iframes': 0,
            'revenue': Decimal(0),
            'clicks': 0,
            'conversions': 0
        }
        for key, value in data.items():
            keys = sum_.keys()
            if key == 'message': continue
            for k,v in value.items():
                if k not in keys:
                    continue
                if isinstance(sum_[k], Decimal):
                    sum_[k] += Decimal(v)
                else:
                    sum_[k] += v


        self.impressions = int(sum_['impressions'])
        self.iframes = int(sum_['iframes'])
        self.revenue = Decimal(sum_['revenue']) / Decimal(self.minicampaign.campaign.fee_percentage / 100)
        self.clicks = int(sum_['clicks'])
        self.conversions = sum_['conversions']
