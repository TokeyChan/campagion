# Generated by Django 3.2.4 on 2021-07-30 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0022_campaign_campagion_budget'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaignstats',
            name='clicks',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='campaignstats',
            name='conversions',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='campaignstats',
            name='ctr',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='campaignstats',
            name='ecpc',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='campaignstats',
            name='ecpm',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='campaignstats',
            name='iframes',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='campaignstats',
            name='impressions',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='campaignstats',
            name='revenue',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=15, null=True),
        ),
    ]
