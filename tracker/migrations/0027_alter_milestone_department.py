# Generated by Django 3.2.4 on 2021-07-23 18:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('tracker', '0026_auto_20210714_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='milestone',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.department'),
        ),
    ]