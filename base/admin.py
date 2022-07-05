from django.contrib import admin
from .models import Tour,Restaurant,Reviews,Hotel,RepairShop,DummyLatLng
# Register your models here.
admin.site.register(Tour)
admin.site.register(Restaurant)
admin.site.register(Reviews)
admin.site.register(Hotel)
admin.site.register(RepairShop)
admin.site.register(DummyLatLng)