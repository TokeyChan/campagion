from main.models import Campaign, MiniCampaign
from main.api_models import CampaignStats
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from datetime import datetime, date

try:
    from traffic_junky.helpers import get_campaign_stats
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
            campaigns = Campaign.objects.exclude(status=Campaign.Status.PRE_ACTIVE)
        else:
            campaigns = Campaign.objects.filter(id__in=campaign_ids)

        for campaign in campaigns:
            start = campaign.start_date
            end = datetime.now().date() if campaign.end_date is None else campaign.end_date

            ids = [child.api_id for child in campaign.children_set.all()]
            stats = get_campaign_stats(settings.API_KEY, ids, start, end)
            for data in stats:
                #hier filtern, ob es überhaupt ein Ergebnis gibt
                minicampaign = MiniCampaign.objects.get(api_id=data['id'])
                try:
                    stats = minicampaign.stats_set.get(date=data['date'])
                except CampaignStats.DoesNotExist:
                    stats = CampaignStats(minicampaign=minicampaign, date=data['date'])
                
                stats.update(data['data'])
                stats.save()

            
