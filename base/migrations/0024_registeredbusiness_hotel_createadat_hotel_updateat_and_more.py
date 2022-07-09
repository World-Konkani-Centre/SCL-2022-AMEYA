# Generated by Django 4.0.5 on 2022-07-03 15:06

import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0023_alter_hotel_rating_alter_repairshop_rating_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegisteredBusiness',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=700)),
                ('description', models.CharField(max_length=500)),
                ('zipcode', models.CharField(max_length=6)),
                ('category', models.CharField(choices=[('1', 'Hospital'), ('2', 'Pharmacy'), ('3', 'Clinic'), ('4', 'Restaurant'), ('5', 'Hotel'), ('6', 'Repair Shop'), ('7', 'Transport')], default='5', max_length=1)),
                ('phone', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=100)),
                ('website', models.CharField(max_length=50, null=True)),
                ('rating', models.FloatField(default=5, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('lat', models.DecimalField(decimal_places=15, max_digits=20)),
                ('lng', models.DecimalField(decimal_places=15, max_digits=20)),
                ('logo', models.ImageField(null=True, upload_to='logos/')),
                ('banner', models.ImageField(null=True, upload_to='banners/')),
                ('createadAt', models.DateTimeField(auto_now_add=True)),
                ('updateAt', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='hotel',
            name='createadAt',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hotel',
            name='updateAt',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='repairshop',
            name='createadAt',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='repairshop',
            name='updateAt',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='createadAt',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='restaurant',
            name='updateAt',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='reviews',
            name='createadAt',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reviews',
            name='updateAt',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='tour',
            name='createadAt',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tour',
            name='updateAt',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='transport',
            name='createadAt',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transport',
            name='updateAt',
            field=models.DateTimeField(auto_now=True),
        ),
    ]