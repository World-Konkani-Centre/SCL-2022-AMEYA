# Generated by Django 4.0.5 on 2022-07-13 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0052_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='profile_pics'),
        ),
    ]
