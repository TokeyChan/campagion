# Generated by Django 3.2.6 on 2021-08-31 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0031_line_is_fallback'),
    ]

    operations = [
        migrations.AddField(
            model_name='milestone',
            name='is_visible',
            field=models.BooleanField(default=True),
        ),
    ]
