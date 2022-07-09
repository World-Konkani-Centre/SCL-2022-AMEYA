from django.contrib import admin
<<<<<<< HEAD
from .models import Tour,Restaurant,Reviews,Hotel,RepairShop,DummyLatLng,RegisteredBusiness,Users
=======
from .models import Tour,Restaurant,Hotel,RepairShop,DummyLatLng,RegisteredBusiness,Users,TourReviews

>>>>>>> 975e7ccb0d42f4179a094f3351ac12244bcfca10
# Register your models here.
admin.site.register(Tour)
admin.site.register(Restaurant)
admin.site.register(TourReviews)
admin.site.register(Hotel)
admin.site.register(Users)
admin.site.register(RepairShop)
admin.site.register(RegisteredBusiness)
admin.site.register(DummyLatLng)
