# Generated by Django 3.2.4 on 2021-07-09 18:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0012_auto_20210708_2305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='milestone',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tracker.milestone'),
        ),
    ]
