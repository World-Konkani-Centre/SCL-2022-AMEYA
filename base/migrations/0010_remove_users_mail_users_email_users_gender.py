# Generated by Django 4.0.5 on 2022-07-07 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_alter_users_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='mail',
        ),
        migrations.AddField(
            model_name='users',
            name='email',
            field=models.EmailField(blank=True, default='', max_length=254),
        ),
        migrations.AddField(
            model_name='users',
            name='gender',
            field=models.CharField(choices=[('1', 'Male'), ('2', 'Female'), ('3', 'Dont want to specify')], default='1', max_length=1),
        ),
    ]
