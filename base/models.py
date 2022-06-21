from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 

# Create your models here.
class Tour(models.Model):
    id=models.BigAutoField(primary_key=True)
    name=models.CharField(max_length=100)
    description=models.CharField(max_length=500)
    rating=models.IntegerField(default=5,validators=[MinValueValidator(1),MaxValueValidator(5)])
    # rating_count=
    avg_fare=models.FloatField(default=0)
    address=models.CharField(max_length=700)
    contact=models.IntegerField(max_length=10)
    hours_open=models.CharField(max_length=100)
    lat=models.DecimalField(max_digits=20,decimal_places=15)
    lng=models.DecimalField(max_digits=20,decimal_places=15)