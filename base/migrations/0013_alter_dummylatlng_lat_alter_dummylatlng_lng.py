# Generated by Django 4.0.5 on 2022-06-29 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_alter_dummylatlng_lat_alter_dummylatlng_lng'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dummylatlng',
            name='lat',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='dummylatlng',
            name='lng',
            field=models.CharField(max_length=20),
        ),
    ]
