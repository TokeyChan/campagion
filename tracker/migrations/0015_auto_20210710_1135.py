# Generated by Django 3.2.4 on 2021-07-10 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0014_auto_20210710_1115'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workflow',
            name='first_date',
        ),
        migrations.AlterField(
            model_name='workflow',
            name='start_date',
            field=models.DateTimeField(null=True),
        ),
    ]
