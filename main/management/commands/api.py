from main.models import Campaign
from main.api_models import CampaignData, CampaignStats
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from datetime import datetime

try:
    from traffic_junky import Member
except ImportError:
    raise ImportError("You need to install the traffic_junky package or put it on your PYTHONPATH")

class Command(BaseCommand):
    help = 'updates the database with data grom the trafficjunky API'

    def add_arguments(self, parser):
        parser.add_argument(
            '--all',
            action="store_true"
        )
        parser.add_argument(
            '--campaign_ids',
            type=int,
            nargs='+'
        )

    def handle(self, *args, **options):
        campaign_ids = options['campaign_ids']
        
        if options['all']:
            campaigns = Campaign.objects.all()
        else:
            campaigns = Campaign.objects.filter(id__in=campaign_ids)
        
        member = Member(settings.API_KEY)

        for campaign in campaigns:
            c = member.get_campaign(id=campaign.api_id) if campaign.api_id is not None else member.get_campaign(name=campaign.name)
            if c is None:
                continue

            if campaign.data is None:
                data = CampaignData()
                data.create(c.data)
                data.save()
                campaign.data = data
                campaign.save()
            else:
                data = campaign.data

            stats = c.stats(end_date=datetime.now())
            if data.stats is None:
                new_stats = CampaignStats()
                new_stats.update(stats)
                new_stats.save()
                data.stats = new_stats
                data.save()
            else:
                data.stats.update(stats)
                data.stats.save()
