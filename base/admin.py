from django.contrib import admin
from .models import Tour,Restaurants,Reviews,Hotel,DummyLatLng,Users
# Register your models here.
admin.site.register(Tour)
admin.site.register(Restaurants)
admin.site.register(Reviews)
admin.site.register(Hotel)
admin.site.register(DummyLatLng)
admin.site.register(Users)