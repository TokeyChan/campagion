# Generated by Django 3.2.4 on 2021-07-03 20:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0004_milestone_color'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='index',
        ),
    ]
