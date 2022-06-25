from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home,name='home'),
    path('index/', views.home,name='home'),
    path('map/',views.map,name='map'),
<<<<<<< HEAD
    path('login/',views.login,name='login'),
    path('signup/',views.signup,name='signup'),
    path('recommendations/',views.recommendations,name='recommendations'),
=======
>>>>>>> 52939a15157ee837b30f3f66fa58a60e13e447df
    path('aboutUs/',views.aboutUs,name='aboutUs'),
    path('contact/',views.contact,name='contact'),
    path('login/',views.login,name='login'),
    path('signup/',views.signup,name='signup'),
    path('recommendations/',views.recommendations,name='recommendations'),
    path('api/v1/tour/<int:id>',views.getTour,name='getTour'),
    path('api/v1/dummy',views.DummyLatLng,name='dummyLatLng'),
    path('trip/',views.trip,name='trip'),
    path('trips/',views.trips,name='trips'),
    path('userProfile/',views.userProfile,name='userProfile'),
    path('tourForm/',views.tourForm,name='tourForm'),
    path('tourDetails/',views.tourDetails,name='tourDetails'),
    path('api/v1/tour/<int:id>',views.getTour,name='getTour'),
    path('api/v1/restaurants/nearby',views.getNearbyRestaurants,name='getNearbyRestaurants'),
    path('api/v1/restaurants/dummy',views.getLatLngs,name='dummyLatLng'),
]

if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)