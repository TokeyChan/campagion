# Generated by Django 3.2.4 on 2021-07-30 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_auto_20210730_1837'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='api_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
