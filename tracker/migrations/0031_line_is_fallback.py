# Generated by Django 3.2.4 on 2021-08-02 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0030_task_fallback_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='line',
            name='is_fallback',
            field=models.BooleanField(default=False),
        ),
    ]
