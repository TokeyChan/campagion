# Generated by Django 3.2.4 on 2021-07-30 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_campaign_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='campagion_budget',
            field=models.DecimalField(decimal_places=2, default=10, max_digits=10),
            preserve_default=False,
        ),
    ]
