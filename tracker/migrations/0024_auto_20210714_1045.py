# Generated by Django 3.2.4 on 2021-07-14 10:45

from django.db import migrations, models
import django.db.models.deletion
import tracker.models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0023_alter_task_workflow'),
    ]

    operations = [
        migrations.AddField(
            model_name='milestone',
            name='upload_dir',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='milestone',
            name='completer',
            field=models.ForeignKey(default=tracker.models.get_click_completer, on_delete=django.db.models.deletion.SET_DEFAULT, to='tracker.completer'),
        ),
    ]