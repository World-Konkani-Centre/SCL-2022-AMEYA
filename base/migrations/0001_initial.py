# Generated by Django 4.0.5 on 2022-06-21 14:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tour',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=500)),
                ('rating', models.IntegerField(default=5, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('avg_fare', models.FloatField(default=0)),
                ('address', models.CharField(max_length=700)),
                ('contact', models.IntegerField(max_length=10)),
                ('hours_open', models.CharField(max_length=100)),
                ('lat', models.DecimalField(decimal_places=15, max_digits=20)),
                ('lng', models.DecimalField(decimal_places=15, max_digits=20)),
            ],
        ),
    ]
