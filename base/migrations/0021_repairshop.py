# Generated by Django 4.0.5 on 2022-07-01 16:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0020_alter_restaurant_rating'),
    ]

    operations = [
        migrations.CreateModel(
            name='RepairShop',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=500)),
                ('rating', models.IntegerField(default=5, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('lat', models.DecimalField(decimal_places=15, max_digits=20)),
                ('lng', models.DecimalField(decimal_places=15, max_digits=20)),
            ],
        ),
    ]