# Generated by Django 3.2.6 on 2021-09-10 21:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0003_commission_is_paid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commission',
            name='is_paid',
        ),
    ]
