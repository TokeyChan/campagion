# Generated by Django 3.2.4 on 2021-07-04 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0005_remove_task_index'),
    ]

    operations = [
        migrations.AddField(
            model_name='workflow',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
