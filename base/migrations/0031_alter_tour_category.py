# Generated by Django 4.0.5 on 2022-07-10 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0030_merge_20220709_2315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tour',
            name='category',
            field=models.CharField(choices=[('1', 'Adventure'), ('2', 'Trekking'), ('3', 'Hiking')], default='1', max_length=1),
        ),
    ]
