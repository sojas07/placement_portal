# Generated by Django 3.0.5 on 2020-11-21 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='studentModel',
            fields=[
                ('registrationId', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True)),
                ('firstName', models.CharField(max_length=100)),
                ('lastName', models.CharField(max_length=100)),
                ('emailId', models.EmailField(max_length=100, unique=True)),
                ('placementSeason', models.CharField(max_length=100)),
                ('jobPlaced', models.CharField(blank=True, max_length=100)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
    ]
