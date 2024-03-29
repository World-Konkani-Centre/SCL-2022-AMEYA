from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0072_tourreviews_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tour',
            name='category',
            field=models.CharField(choices=[('1', 'Adventure'), ('2', 'Trekking'), ('3', 'Hiking'), ('4', 'Historical'), ('5', 'Wildlife'), ('6', 'Religious'), ('7', 'Relaxation')], default='1', max_length=1),
        ),
    ]
