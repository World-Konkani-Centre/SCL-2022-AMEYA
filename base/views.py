from django.shortcuts import render
from django.http import JsonResponse
from django.core.serializers import serialize
from .models import DummyLatLng, Tour,Restaurant,Hotel,RepairShop
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
    context={'tour':tour}
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

# method to get nearby restaurants,hotels and repair shops:
@csrf_exempt
def getNearby(request,cat):
    nearby=[]
    body=json.loads(request.body.decode('utf-8'))
    routeCoords=body['routeCoordinates']
    tourCoords=body['tourCoordinates']
    centerCoord=body['center']
    # Calculate radius of center:
    radius=haversine((centerCoord[0],centerCoord[1]),(tourCoords[0][0],tourCoords[0][1]))+50
    if(cat=='hotel'):
        query=Hotel.objects.all()
    elif(cat=='restaurant'):
        query=Restaurant.objects.all()
    elif(cat=='repair'):
        query=RepairShop.objects.all()

    locFiltered=[loc for loc in query if haversine((loc.lat,loc.lng),(centerCoord[0],centerCoord[1]))<=radius]
    for item in locFiltered:
        for route in routeCoords:
            if haversine((item.lat,item.lng),(route["lat"],route["lng"]),unit=Unit.KILOMETERS)<=3:
                nearby.append(item)
                break
    data=serialize('json',nearby)
    return JsonResponse(data,safe=False)
