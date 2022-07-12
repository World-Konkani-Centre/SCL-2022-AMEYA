from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from PIL import Image
# Tour model:
class Tour(models.Model):
    category_choices=[('1','Adventure'),('2','Trekking'),('3','Hiking')]
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
    createadAt=models.DateTimeField(auto_now_add=True)
    updateAt=models.DateTimeField(auto_now=True)
    image=models.ImageField(upload_to='images/recommendation',null=True)

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
    createadAt=models.DateTimeField(auto_now_add=True)
    updateAt=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    id=models.BigAutoField(primary_key=True)
    role_choices=[('1','User'),('2','Business')]
    gender_choices=[('1','Male'),('2','Female'),('3','Dont want to specify')]
    gender=models.CharField(blank=True, max_length=1,choices=gender_choices,default='1')
    phone=models.CharField(blank=True, max_length=10,default='')
    DOB=models.DateField(blank=True,default='2001-01-01')
    role=models.CharField(blank=True, max_length=1,choices=role_choices,default='1')
    image=models.ImageField(upload_to='profile_pics', height_field=None, width_field=None, max_length=100,default='default.jpg')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        
        img= Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)






        
# Reviews model:
class TourReviews(models.Model):
    id=models.BigAutoField(primary_key=True)
    tour=models.ForeignKey(Tour,on_delete=models.CASCADE)
    # user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    rating=models.IntegerField(default=5,validators=[MinValueValidator(1),MaxValueValidator(5)])
    review=models.CharField(max_length=500)
    createadAt=models.DateTimeField(auto_now_add=True)
    updateAt=models.DateTimeField(auto_now=True)


# Hotel model:
class Hotel(models.Model):
    id=models.BigAutoField(primary_key=True)
    name=models.CharField(max_length=100)
    description=models.CharField(max_length=500)
    website=models.CharField(max_length=50,default="www.google.com")
    rating=models.FloatField(default=5,validators=[MinValueValidator(1),MaxValueValidator(5)])
    lat=models.DecimalField(max_digits=20,decimal_places=15)
    lng=models.DecimalField(max_digits=20,decimal_places=15)
    createadAt=models.DateTimeField(auto_now_add=True)
    updateAt=models.DateTimeField(auto_now=True)

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
    createadAt=models.DateTimeField(auto_now_add=True)
    updateAt=models.DateTimeField(auto_now=True)

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
    createadAt=models.DateTimeField(auto_now_add=True)
    updateAt=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# Registered Business model:
class RegisteredBusiness(models.Model):
    category_choices=[('1','Restaurant'),('2','Hotel'),('3','Clinic'),('4','Hospital'),('5','Pharmacy'),('6','Repair Shop'),('7','Travel')]
    id=models.BigAutoField(primary_key=True)
    name=models.CharField(max_length=100)
    address=models.CharField(max_length=700)
    description=models.CharField(max_length=500)
    zipcode=models.CharField(max_length=6)
    category=models.CharField(max_length=1,choices=category_choices,default='5')
    phone=models.CharField(max_length=10)
    email=models.EmailField(max_length=100)
    website=models.CharField(max_length=50,null=True)
    rating=models.FloatField(default=5,validators=[MinValueValidator(1),MaxValueValidator(5)],null=True)
    lat=models.DecimalField(max_digits=20,decimal_places=15)
    lng=models.DecimalField(max_digits=20,decimal_places=15)
    logo=models.ImageField(upload_to='images/regBiz',null=True)
    banner=models.ImageField(upload_to='images/regBiz',null=True)
    createadAt=models.DateTimeField(auto_now_add=True)
    updateAt=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

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
