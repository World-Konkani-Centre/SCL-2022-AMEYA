# Generated by Django 4.0.5 on 2022-07-06 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_alter_dummylatlng_latlng'),
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('firstname', models.CharField(max_length=255)),
                ('lastname', models.CharField(max_length=255)),
                ('username', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=50)),
                ('DOB', models.DateTimeField()),
                ('phone', models.IntegerField(verbose_name='max_length=10')),
                ('profile', models.ImageField(upload_to=None)),
            ],
        ),
    ]
