from django.contrib import admin
from .models import Tour,RegisteredBusiness,Profile,TourReviews,Business
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(Tour)
admin.site.register(TourReviews)
admin.site.register(RegisteredBusiness)
admin.site.register(Profile)
admin.site.register(Business)

class ProfileInline(admin.StackedInline):
    model=Profile
    can_delete=False
    verbose_name_plural='Profile'

class UserAdmin(UserAdmin):
    inlines=(ProfileInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)


