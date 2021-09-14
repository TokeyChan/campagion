from django.db.models import Sum, Avg
from main.models import Campaign, MiniCampaign
from django.http import JsonResponse
from datetime import datetime, timedelta
from main.contrib.api import calc_statistics
import json

def api_minicampaigns(request):
    campaign_id = request.GET.get('campaign_id')
    minicampaigns = MiniCampaign.objects.filter(campaign_id=campaign_id)
    list_ = [{
        'id': m.id,
        'name': m.name
    } for m in minicampaigns]
    return JsonResponse(list_, safe=False)

def api_sum_campaign(request):
    campaign_id = request.GET.get('campaign_id')
    campaign = Campaign.objects.get(id=campaign_id)
    minicampaigns = campaign.children_set.all()
    data = {}

    for minicampaign in minicampaigns:
        result = minicampaign.get_stats()

        if len(data.keys()) == 0:
            data = result
        else:
            for k, v in result.items():
                data[k] += v
    
    data = calc_statistics(data)
    data['revenue'] = float(round(data['revenue'], 2))
    return JsonResponse(data)

def api_sum_minicampaign(request):
    minicampaign_id = request.GET.get('minicampaign_id')
    mini = MiniCampaign.objects.get(id=minicampaign_id)
    stats = mini.get_stats()
    stats = calc_statistics(stats)
    stats['revenue'] = float(round(stats['revenue'], 2))
    return JsonResponse(stats)


def api_stats_campaign(request):
    if request.method == 'POST':
        raise ValueError("This view should never be accessed via POST")

    campaign_id = request.GET.get('campaign_id')
    campaign = Campaign.objects.get(id=campaign_id)

    get_start_date = request.GET.get('start_date')
    get_end_date = request.GET.get('end_date')
    if get_start_date is None or get_end_date is None:
        return JsonResponse({'error': 'neither start_date or end_date may be ommitted'})
        
    start_date = datetime.strptime(get_start_date, "%d/%m/%Y").date()
    end_date = datetime.strptime(get_end_date, "%d/%m/%Y").date()

    results = []
    for minicampaign in campaign.children_set.all():
        results.append(minicampaign.stats_set.filter(date__gte=start_date, date__lte=end_date))

    if len(results) == 0:
        return JsonResponse({})

    qs = results[0]
    for i in range(1, len(results)):
        qs = qs | results[i]

    datasets = {
        'impressions': {
            'label': 'Impressions',
            'data': []
        },
        'revenue': {
            'label': 'Ausgaben',
            'data': []
        },
        'clicks': {
            'label': 'Clicks',
            'data': []
        },
        'ctr': {
            'label': 'CTR',
            'data': []
        },
        'ecpm': {
            'label': 'eCPM',
            'data': []
        },
        'ecpc': {
            'label': 'eCPC',
            'data': []
        },
        'conversions': {
            'label': 'Conversions',
            'data': []
        }
    }
    while start_date <= end_date:
        print(start_date)
        stats = qs.filter(date=start_date).aggregate(
            impressions = Sum('impressions'),
            revenue = Sum('revenue'),
            clicks = Sum('clicks'),
            conversions = Sum('conversions')
        )
        stats = calc_statistics(stats)
        for key in stats.keys():
            if stats[key] is not None:
                datasets[key]['data'].append({'x': start_date.strftime('%d.%m'), 'y': round(stats[key], 4)})
            else:
                datasets[key]['data'].append({'x': start_date.strftime('%d.%m'), 'y': None})

        start_date += timedelta(days=1)

    return JsonResponse({
        'campaign_id': campaign_id,
        'minicampaign': '__all__',
        'datasets': [value for value in datasets.values()]
    })

def api_stats_minicampaign(request, minicampaign_id):
    pass