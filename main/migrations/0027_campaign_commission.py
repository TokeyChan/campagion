# Generated by Django 3.2.6 on 2021-09-02 13:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0001_initial'),
        ('main', '0026_alter_campaign_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='commission',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='administration.commission'),
        ),
    ]
