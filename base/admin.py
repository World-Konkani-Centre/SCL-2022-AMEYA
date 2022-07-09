from django.contrib import admin
<<<<<<< HEAD
from .models import Tour,Restaurants,Reviews,Hotel,DummyLatLng,Users
=======
from .models import Tour,Restaurant,Reviews,Hotel,RepairShop,DummyLatLng,RegisteredBusiness,Users
>>>>>>> main
# Register your models here.
admin.site.register(Tour)
admin.site.register(Restaurant)
admin.site.register(Reviews)
admin.site.register(Hotel)
<<<<<<< HEAD
admin.site.register(DummyLatLng)
admin.site.register(Users)
=======
admin.site.register(Users)
admin.site.register(RepairShop)
admin.site.register(RegisteredBusiness)
admin.site.register(DummyLatLng)
>>>>>>> main
