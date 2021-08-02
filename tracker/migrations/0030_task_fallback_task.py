# Generated by Django 3.2.4 on 2021-08-02 07:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0029_auto_20210725_2024'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='fallback_task',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tracker.task'),
        ),
    ]
