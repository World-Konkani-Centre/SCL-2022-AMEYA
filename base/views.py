from django.shortcuts import render

# Create your views here.
def home(request):
    context={'name':"Kishor"}
    return render(request,"base/home.html",context)

def map(request):
    context={}
    return render(request,"base/map.html",context)

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