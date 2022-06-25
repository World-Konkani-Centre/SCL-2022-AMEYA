from django.shortcuts import render
from django.http import JsonResponse
from django.core.serializers import serialize
from .models import DummyLatLng, Tour,Restaurants
from haversine import haversine,Unit
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
def home(request):
    context={'name':"Kishor"}
    return render(request,"base/home.html",context)

def map(request):
    id=request.GET.get('id',1)
    tour=Tour.objects.get(id=id)
    context={'tour':tour,'distance':haversine((tour.lat,tour.lng),(13.00918844987077,77.59796068053168),unit=Unit.METERS)}
    return render(request,"base/map.html",context)

def getTour(request,id):
    tour=Tour.objects.get(id=id)
    data=serialize('json',[tour])
    return JsonResponse(data,safe=False)

def login(request):
    context={}
    return render(request,"base/login.html",context)

def signup(request):
    context={}
    return render(request,"base/signup.html",context)

def recommendations(request):
    context={}
    return render(request,"base/recommendations.html",context)

def aboutUs(request):
    context={}
    return render(request,"base/aboutUs.html",context)

def contact(request):
    context={}
    return render(request,"base/contact.html",context)

def tourDetails(request):
    context={}
    return render(request,"base/tourDetails.html",context)

def tourForm(request):
    context={}
    return render(request,"base/tourForm.html",context)

def trip(request):
    context={}
    return render(request,"base/trip.html",context)

def trips(request):
    context={}
    return render(request,"base/trips.html",context)

def userProfile(request):
    context={}
    return render(request,"base/userProfile.html",context)


# Dummy data API:
def getLatLngs(request):
    latlng=DummyLatLng.objects.all()
    data=serialize('json',latlng)
    return JsonResponse(data,safe=False)

# method to get nearby restaurants
@csrf_exempt
def getNearbyRestaurants(request):
    latLngs=json.loads(request.body.decode('utf-8'))
    latlng=DummyLatLng.objects.values_list('latLng', flat=True)
    print(list(latlng))
    data=serialize('json',[latlng])
    return JsonResponse(data,safe=False)
