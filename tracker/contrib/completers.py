from datetime import datetime

from django.shortcuts import redirect, reverse
from django.http import HttpResponseRedirect
from django.conf import settings

from administration.models import Commission
from month import Month
from decimal import Decimal

class Completer:
    def __init__(self, request, task, url):
        self.task = task
        self.url = url
        self.request = request

    def complete(self):
        self.task.workflow.complete_task(self.task)
        if self.task.milestone.name == settings.COMMISSION_MILESTONE_NAME:
            create_commission(self.task)
    
class ClickCompleter(Completer):
    def handle(self):
        self.complete()
        return redirect(self.url)

class UploadCompleter(Completer):
    def handle(self):
        return redirect('tracker:upload_file', task_id=self.task.id)

def create_commission(task):
    user = task.assigned_user()
    month = Month.from_date(datetime.now())
    campaign = task.workflow.campaign

    try:
        commission = Commission.objects.get(user=user, month=month)
    except Commission.DoesNotExist:
        commission = Commission(user=user, month=month, amount=0)
    
    commission.amount += campaign.commission_amount()
    commission.save()

    campaign.commission = commission
    campaign.save()
    

