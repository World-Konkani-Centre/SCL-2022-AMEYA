# Generated by Django 4.0.5 on 2022-07-13 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0055_alter_profile_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(choices=[('1', 'Male'), ('2', 'Female'), ('3', 'Dont want to specify')], default='1', max_length=1),
        ),
        migrations.AlterField(
            model_name='profile',
            name='role',
            field=models.CharField(choices=[('1', 'User'), ('2', 'Business')], default='1', max_length=1),
        ),
    ]