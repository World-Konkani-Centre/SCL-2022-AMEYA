import profile
from django.db import models
from django.db.models import Avg
from django.core.validators import MaxValueValidator, MinValueValidator,validate_comma_separated_integer_list
from django.contrib.auth.models import User
from PIL import Image
# Tour model:
class Tour(models.Model):
    category_choices=[('1','Adventure'),('2','Trekking'),('3','Hiking'),('4','Historical'),('5','Wildlife'),('6','Religious'),('7','Relaxation')]
    category_choices1=[('1','Bangalore'),('2','Dakshina Kannada'),('3','Udupi'),('4','Uttara Kannada')]
    id=models.BigAutoField(primary_key=True)
    name=models.CharField(max_length=100)
    place=models.CharField(max_length=1,choices=category_choices1,default='1')
    description=models.CharField(max_length=500)
    website=models.CharField(max_length=50,blank=True,default='')
    category=models.CharField(max_length=1,choices=category_choices,default='1')
    rating=models.FloatField(default=5,validators=[MinValueValidator(1),MaxValueValidator(5)])
    avg_fare=models.FloatField(default=0)
    address=models.CharField(max_length=700)
    contact=models.CharField(max_length=10,blank=True,default='')
    hours_open=models.CharField(max_length=300,blank=True,default='')
    lat=models.DecimalField(max_digits=20,decimal_places=15)
    lng=models.DecimalField(max_digits=20,decimal_places=15)
    places_nearby=models.CharField(max_length=500,blank=True,default='')
    instructions=models.CharField(max_length=500,blank=True,default='')
    createadAt=models.DateTimeField(auto_now_add=True)
    updateAt=models.DateTimeField(auto_now=True)
    image=models.ImageField(upload_to='images/recommendation',null=True,blank=True)
    subtext=models.CharField(max_length=200,default='')
    date = models.CharField(validators=[validate_comma_separated_integer_list],max_length=200, blank=True, null=True,default='')

    # Calculate the average rating of the tour from TourReview model:
    def get_avg_rating(self):
        rating=TourReviews.objects.filter(tour=self).aggregate(Avg('rating'))['rating__avg']
        if rating:
            return round(rating,1)
        else:
            return 1.0
    
    def calc_avg_rating(self):
        rating=TourReviews.objects.filter(tour=self).aggregate(Avg('rating'))['rating__avg']
        if rating:
            self.rating=round(rating,1)
        else:
            self.rating=1.0
        self.save()

    def __str__(self):
        return self.name

class Profile(models.Model):
    gender_choices=[('1','Male'),('2','Female'),('3','Dont want to specify')]
    id=models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    gender=models.CharField(max_length=1,choices=gender_choices,default='1')
    phone=models.CharField(blank=True, max_length=10,default='')
    DOB=models.DateField(null=True)
    image=models.ImageField(blank=True,upload_to='images/user', height_field=None, width_field=None, max_length=100,null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        if(self.image):
            img= Image.open(self.image.path)    
            if img.height > 300 or img.width > 300:
                output_size = (300,300)
                img.thumbnail(output_size)
                img.save(self.image.path)

# Tour Reviews model:
class TourReviews(models.Model):
    id=models.BigAutoField(primary_key=True)
    tour=models.ForeignKey(Tour,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE,default="")
    rating=models.IntegerField(default=5,validators=[MinValueValidator(1),MaxValueValidator(5)])
    review=models.CharField(max_length=500)
    createadAt=models.DateTimeField(auto_now_add=True)
    updateAt=models.DateTimeField(auto_now=True)

# Tour Wishlist model:
class Wishlist(models.Model):
    id=models.BigAutoField(primary_key=True)
    tour=models.ForeignKey(Tour,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    createadAt=models.DateTimeField(auto_now_add=True)
    updateAt=models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)
        
# Businesses model:
class Business(models.Model):
    category_choices=[('restaurant','Restaurant'),('hotel','Hotel'),('repair','Repair'),('transport','Transport'),('shoping','Shoping'),('gas','Gas'),('parking','Parking'),('bank','Bank')]
    id=models.BigAutoField(primary_key=True)
    name=models.CharField(max_length=100)
    type=models.BooleanField(default=False)
    category=models.CharField(max_length=100,choices=category_choices,default='restaurant')
    description=models.CharField(max_length=500)
    website=models.CharField(max_length=50,blank=True)
    rating=models.FloatField(default=5,validators=[MinValueValidator(1),MaxValueValidator(5)])
    lat=models.DecimalField(max_digits=20,decimal_places=15)
    lng=models.DecimalField(max_digits=20,decimal_places=15)
    createadAt=models.DateTimeField(auto_now_add=True)
    updateAt=models.DateTimeField(auto_now=True)
    image=models.ImageField(blank=True,upload_to='images/business',null=True)

    def __str__(self):
        return self.name

# Registered Business model:
class RegisteredBusiness(models.Model):
    category_choices=[('restaurant','Restaurant'),('hotel','Hotel'),('repair','Repair'),('transport','Transport'),('shoping','Shoping'),('gas','Gas'),('parking','Parking'),('bank','Bank')]
    id=models.BigAutoField(primary_key=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,default='')
    name=models.CharField(max_length=100)
    type=models.BooleanField(default=True)
    address=models.CharField(max_length=700)
    description=models.CharField(max_length=500)
    zipcode=models.CharField(max_length=6)
    category=models.CharField(max_length=100,choices=category_choices,default='restaurant')
    phone=models.CharField(max_length=10,blank=True)
    email=models.EmailField(max_length=100)
    website=models.CharField(max_length=50,null=True,blank=True)
    rating=models.FloatField(default=5,validators=[MinValueValidator(1),MaxValueValidator(5)],null=True)
    lat=models.DecimalField(max_digits=20,decimal_places=15)
    lng=models.DecimalField(max_digits=20,decimal_places=15)
    logo=models.ImageField(upload_to='images/regBiz',null=True,blank=True)
    banner=models.ImageField(upload_to='images/regBiz',null=True,blank=True)
    createadAt=models.DateTimeField(auto_now_add=True)
    updateAt=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# Saved Tour model:
class SavedTour(models.Model):
    id=models.BigAutoField(primary_key=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    tour=models.ForeignKey(Tour,on_delete=models.CASCADE)
    tourCoords=models.CharField(max_length=2000)
    tourRoute=models.CharField(max_length=2000)
    createadAt=models.DateTimeField(auto_now_add=True)
    updateAt=models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)
        
#Newsletter
class Subscribers(models.Model):
    email=models.EmailField(null=True)
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class MailMessage(models.Model):
    title=models.CharField(max_length=100)
    message=models.TextField(null=True)

    def __str__(self):
        return self.title

