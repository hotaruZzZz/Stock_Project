# Generated by Django 4.1 on 2022-10-26 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': (('can_comment', 'Can comment'),),
            },
        ),
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sName', models.CharField(max_length=20)),
                ('sNumber', models.CharField(max_length=20)),
                ('sDate', models.DateField()),
                ('sOpen', models.DecimalField(decimal_places=2, max_digits=20)),
                ('sHigh', models.DecimalField(decimal_places=2, max_digits=20)),
                ('sLow', models.DecimalField(decimal_places=2, max_digits=20)),
                ('sClose', models.DecimalField(decimal_places=2, max_digits=20)),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default='', max_length=20)),
                ('name', models.CharField(default='', max_length=20)),
                ('type', models.CharField(default='', max_length=30)),
                ('ISIN', models.CharField(default='', max_length=20)),
                ('market', models.CharField(default='', max_length=20)),
                ('group', models.CharField(default='', max_length=20)),
            ],
        ),
    ]
