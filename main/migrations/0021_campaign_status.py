# Generated by Django 3.2.4 on 2021-07-30 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_auto_20210730_2043'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='status',
            field=models.IntegerField(choices=[(1, 'Pre Active'), (2, 'Active'), (3, 'Not Active')], default=1),
        ),
    ]