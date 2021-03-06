# Generated by Django 3.2.4 on 2021-07-31 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_auto_20210730_2205'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaignstats',
            name='last_update',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='status',
            field=models.IntegerField(choices=[(1, 'Pre Active'), (2, 'Active'), (3, 'Finished')], default=1),
        ),
    ]
