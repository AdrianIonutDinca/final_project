# Generated by Django 4.2 on 2025-01-23 17:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0013_selecteddata_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='selecteddata',
            name='created_at',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]
