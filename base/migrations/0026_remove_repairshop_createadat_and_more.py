# Generated by Django 4.0.5 on 2022-07-05 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0025_merge_20220705_2134'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='repairshop',
            name='createadAt',
        ),
        migrations.RemoveField(
            model_name='repairshop',
            name='updateAt',
        ),
        migrations.RemoveField(
            model_name='transport',
            name='createadAt',
        ),
        migrations.RemoveField(
            model_name='transport',
            name='updateAt',
        ),
        migrations.AlterField(
            model_name='registeredbusiness',
            name='category',
            field=models.CharField(choices=[('1', 'Restaurant'), ('2', 'Hotel'), ('3', 'Clinic'), ('4', 'Hospital'), ('5', 'Pharmacy'), ('6', 'Repair Shop'), ('7', 'Travel')], default='5', max_length=1),
        ),
    ]
