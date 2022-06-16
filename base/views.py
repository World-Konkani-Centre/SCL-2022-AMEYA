from django.shortcuts import render

# Create your views here.
def home(request):
    context={'name':"Kishor"}
    return render(request,"base/home.html",context)

def map(request):
    context={}
    return render(request,"base/map.html",context)