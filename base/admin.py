from django.contrib import admin
from .models import Tour,Restaurant,TourReviews,Hotel,RepairShop,DummyLatLng,RegisteredBusiness
# Register your models here.
admin.site.register(Tour)
admin.site.register(Restaurant)
admin.site.register(TourReviews)
admin.site.register(Hotel)
admin.site.register(RepairShop)
admin.site.register(RegisteredBusiness)
admin.site.register(DummyLatLng)