# Generated by Django 5.1.1 on 2024-10-19 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Medapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='city_table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('stateISO', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('countryISO', models.CharField(max_length=100)),
            ],
        ),
    ]
