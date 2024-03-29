# Generated by Django 4.0.5 on 2022-08-17 11:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0077_merge_0074_remove_profile_role_0076_alter_tour_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='SavedTour',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('tourCoords', models.CharField(max_length=2000)),
                ('tourRoute', models.CharField(max_length=2000)),
                ('createadAt', models.DateTimeField(auto_now_add=True)),
                ('updateAt', models.DateTimeField(auto_now=True)),
                ('tour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.tour')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
