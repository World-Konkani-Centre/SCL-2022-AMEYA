from unicodedata import category
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 

# Tour model:
class Tour(models.Model):
    category_choices=[('1','Hiking'),('2','Trekking'),('3','Adventure')]
    id=models.BigAutoField(primary_key=True)
    name=models.CharField(max_length=100)
    description=models.CharField(max_length=500)
    website=models.CharField(max_length=50,default="www.google.com")
    category=models.CharField(max_length=1,choices=category_choices,default='1')
    rating=models.FloatField(default=5,validators=[MinValueValidator(1),MaxValueValidator(5)])
    # rating_count=
    avg_fare=models.FloatField(default=0)
    address=models.CharField(max_length=700)
    contact=models.CharField(max_length=10)
    hours_open=models.CharField(max_length=100)
    lat=models.DecimalField(max_digits=20,decimal_places=15)
    lng=models.DecimalField(max_digits=20,decimal_places=15)

    def __str__(self):
        return self.name

# Restaurant model:
class Restaurant(models.Model):
    id=models.BigAutoField(primary_key=True)
    name=models.CharField(max_length=100)
    description=models.CharField(max_length=500)
    rating=models.FloatField(default=5,validators=[MinValueValidator(1),MaxValueValidator(5)])
    lat=models.DecimalField(max_digits=20,decimal_places=15)
    lng=models.DecimalField(max_digits=20,decimal_places=15)

    def __str__(self):
        return self.name

# Reviews model:
class Reviews(models.Model):
    id=models.BigAutoField(primary_key=True)
    tour_id=models.ForeignKey(Tour,on_delete=models.CASCADE)
    # user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    rating=models.IntegerField(default=5,validators=[MinValueValidator(1),MaxValueValidator(5)])
    review=models.CharField(max_length=500)
    date=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.id

# Hotel model:
class Hotel(models.Model):
    id=models.BigAutoField(primary_key=True)
    name=models.CharField(max_length=100)
    description=models.CharField(max_length=500)
    website=models.CharField(max_length=50,default="www.google.com")
    rating=models.FloatField(default=5,validators=[MinValueValidator(1),MaxValueValidator(5)])
    lat=models.DecimalField(max_digits=20,decimal_places=15)
    lng=models.DecimalField(max_digits=20,decimal_places=15)

    def __str__(self):
        return self.name
        
# Repair shop model:
class RepairShop(models.Model):
    id=models.BigAutoField(primary_key=True)
    name=models.CharField(max_length=100)
    description=models.CharField(max_length=500)
    rating=models.FloatField(default=5,validators=[MinValueValidator(1),MaxValueValidator(5)])
    lat=models.DecimalField(max_digits=20,decimal_places=15)
    lng=models.DecimalField(max_digits=20,decimal_places=15)

    def __str__(self):
        return self.name

# Transport model:
class Transport(models.Model):
    id=models.BigAutoField(primary_key=True)
    name=models.CharField(max_length=100)
    description=models.CharField(max_length=500)
    rating=models.FloatField(default=5,validators=[MinValueValidator(1),MaxValueValidator(5)])
    lat=models.DecimalField(max_digits=20,decimal_places=15)
    lng=models.DecimalField(max_digits=20,decimal_places=15)

    def __str__(self):
        return self.name

class DummyLatLng(models.Model):
    lat=models.DecimalField(max_digits=20,decimal_places=15)
    lng=models.DecimalField(max_digits=20,decimal_places=15)
