# Generated by Django 4.0.5 on 2022-07-12 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0044_alter_profile_gender_alter_profile_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='DOB',
            field=models.DateField(blank=True),
        ),
    ]