# Generated by Django 4.0.5 on 2022-07-10 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0034_remove_profile_dob_remove_profile_country_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
