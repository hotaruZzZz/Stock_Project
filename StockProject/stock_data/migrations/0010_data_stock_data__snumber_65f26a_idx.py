# Generated by Django 4.1 on 2022-12-29 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_data', '0009_technicalside'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='data',
            index=models.Index(fields=['sNumber', 'sName'], name='stock_data__sNumber_65f26a_idx'),
        ),
    ]
