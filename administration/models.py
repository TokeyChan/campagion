from django.db import models
from datetime import datetime
from month import Month
from month.models import MonthField

import json

# Create your models here.

class CommissionManager(models.Manager):
    def get_from_user_and_months(self, user, months):
        result = {}
        now = datetime.now()
        current_month = Month.from_date(now)

        for month in months:
            try:
                commission = Commission.objects.get(user=user, month=month)
                result[month.month] = commission
            except Commission.DoesNotExist:
                result[month.month] = None

        return result


class Commission(models.Model):
    user = models.ForeignKey("main.User", on_delete=models.CASCADE)
    month = MonthField()
    amount = models.DecimalField(max_digits=7, decimal_places=2)

    objects = CommissionManager()

    def to_json(self):
        data = {
            'year': self.month.year,
            'month': self.month.month,
            'amount': float(round(self.amount, 2)),
            'campaigns': []
        }
        for campaign in self.campaign_set.all():
            data['campaigns'].append({
                'id': campaign.id,
                'name': campaign.name,
                'budget': float(round(campaign.budget, 2)),
                'campagion_budget': float(round(campaign.campagion_budget, 2)),
                'client': campaign.client.name,
                'commission_amount': float(campaign.commission_amount())
            })
        return data