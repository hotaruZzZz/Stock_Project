# Generated by Django 4.1 on 2022-11-13 14:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock_data', '0005_alter_monthlyrevenue_month_alter_monthlyrevenue_year'),
    ]

    operations = [
        migrations.RenameField(
            model_name='monthlyrevenue',
            old_name='month',
            new_name='Mmonth',
        ),
        migrations.RenameField(
            model_name='monthlyrevenue',
            old_name='year',
            new_name='Myear',
        ),
    ]