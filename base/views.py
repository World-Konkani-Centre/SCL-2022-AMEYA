from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.core.serializers import serialize
from django.contrib import messages
from .models import RegisteredBusiness,Tour,Business,TourReviews,Wishlist,Profile,Subscribers,SavedTour
from haversine import haversine,Unit
from django.template.defaulttags import register
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout,update_session_auth_hash
from .forms import UserUpdateForm, ProfileUpdateForm , PasswordChangingForm,SubscribersForm,MailMessageForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMultiAlternatives,send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .serializers import BusinessSerializer,RegisteredBusinessSerializer
from rest_framework.response import Response
from django.core.paginator import Paginator
from django_pandas.io import read_frame
import datetime

# Create your views here.

def home(request):
    context={'name':"Kishor"}
    return render(request,"base/home.html",context)

def map(request):
    id=request.GET.get('id',1)
    tour=Tour.objects.get(id=id)
    context={'tour':tour}
    if request.user.is_authenticated:
        user=request.user
        if Wishlist.objects.filter(user=user,tour=tour).exists():
            wishlist=True
        else:
            wishlist=False
        context['wishlist']=wishlist
    return render(request,"base/map.html",context)

def getTour(request,id):
    tour=Tour.objects.get(id=id)
    tour.calc_avg_rating()
    data=serialize('json',[tour])
    return JsonResponse(data,safe=False)

def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST': 
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        email=email.rstrip()

        if email == '' or password == '' or username == '':
            messages.error(request,"Please fill all the fields.")
            return render(request,"base/signup.html")
        
        if User.objects.filter(username=username).exists(): 
            messages.add_message(request, messages.INFO, 'Username already exists.')
            return render(request,"base/signup.html")

        elif User.objects.filter(email=email).exists():
            messages.add_message(request, messages.INFO, 'Email already exists.')
            return render(request,"base/signup.html")

        else :
            user = User.objects.create(email=email, username=username, password=make_password(password))
            user.save() 
            auth_login(request, user)    
            html_content = render_to_string('base/email/email.html',{'title':'Welcome to Yatra Mitra App','message':'Welcome to  Yatra Mitra app. Thank you for signing up.','name':username})
            text_content = strip_tags(html_content)
            email_content = EmailMultiAlternatives('Welcome to Yatra Mitra App', text_content, settings.EMAIL_HOST_USER, [email])
            email_content.attach_alternative(html_content, "text/html")
            email_content.send()
            messages.add_message(request, messages.INFO, 'You have successfully signed up.')
            return redirect('/')
    else:
        return render(request,"base/signup.html")

def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST': 
        login_username=request.POST['usernamel']
        login_password=request.POST['passwordl']
        user = authenticate(request, username = login_username, password = login_password)
        if user is not None:
            auth_login(request, user)
            messages.add_message(request, messages.INFO, 'You have successfully logged in.')
            return redirect('/')
        else:
            messages.add_message(request, messages.INFO, 'Invalid username or password.')
            return render(request,"base/login.html")
    return render(request,"base/login.html")

def logout(request):
    auth_logout(request)
    messages.info(request,'You logged out.')
    return redirect('/')

def recommendations(request):
    tour_data=Tour.objects.get_queryset()
    if request.method=='POST':
        category1= request.POST['category']  
        category2=request.POST['place'] 
        start_date=request.POST['startdate']
        end_date=request.POST['enddate']
        datem1 = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        datem2 = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        start_month=datem1.month
        end_month=datem2.month
        tour_data = tour_data.filter(category=category1,place=category2)
        if(start_month>end_month):
            start_month=1
        for i in range(start_month,end_month+1):
            tour_data=tour_data.filter(date__icontains=i)

        if not tour_data:
            messages.error(request,"Sorry! We couldn't find recommmendations of your choice!")
            return render(request,"base/tourForm.html")
    
    for tour in tour_data:
        tour.calc_avg_rating()
    tour_data=tour_data.order_by('-rating')
    paginator = Paginator(tour_data, 5) 
    page = request.GET.get('page')
    tour_data = paginator.get_page(page)
    context={'tour_data':tour_data}
    return render(request,"base/recommendations.html",context)

def aboutUs(request):
    context={}
    return render(request,"base/aboutUs.html",context)

def contact(request):
    if request.method =="POST":
        contact_name = request.POST['contact-name']
        contact_email = request.POST['contact-email']
        contact_message = request.POST['contact-message']
        # send email
        send_mail(
            'Message from ' + contact_name + ', regarding Yatra Mitra', # subject
            contact_message, # message
            contact_email, # From mail 
            ['yatramitra.app@gmail.com'], # To email
        )
        messages.add_message(request, messages.INFO, 'Your message has been sent successfully.')
        return redirect('/')
   
    else:
        context={}
        return render(request,"base/contact.html",context)

def tourDetails(request,id):
    tour=Tour.objects.get(id=id)
    tourData=Tour.objects.filter(id=id).values()[0]
    context={}
    # Open hours:
    hours=tourData['hours_open']
    tourData['hours_open']=hours.split(',')
    # Avg rating:
    tourData['rating']=tour.get_avg_rating()
    context['data']=tourData
    # Wishlist:
    if request.user.is_authenticated:
        user=request.user
        if Wishlist.objects.filter(user=user,tour=tour).exists():
            wishlist=True
        else:
            wishlist=False
        context['wishlist']=wishlist
    # Reviews:
    reviews=TourReviews.objects.filter(tour=tour).order_by('-rating')
    # Reviews pagination:
    paginator = Paginator(reviews, 5) # Show 5 reviews per page
    page = request.GET.get('page')
    reviews = paginator.get_page(page)
    context['reviews']=reviews
    return render(request,"base/tourDetails.html",context)

def tourForm(request):
    context={}
    return render(request,"base/tourForm.html",context)

@login_required
def tourReview(request,id):
    tour=Tour.objects.get(id=id)
    tour.calc_avg_rating()
    context={'tour':tour}
    user=request.user
    # Submit review:
    if request.method=='POST':
        rating=request.POST.get('rating')
        review=request.POST.get('review')
        if(rating==None): rating=1
        if(TourReviews.objects.filter(user=user,tour=tour).exists()):
            rev=TourReviews.objects.get(user=user,tour=tour)
            rev.rating=rating
            rev.review=review
            rev.save()
            messages.add_message(request, messages.INFO, 'Your Review has been updated.')
        else:
            TourReviews.objects.create(user=user,tour=tour,rating=rating,review=review)
            messages.add_message(request, messages.SUCCESS, 'Your Review has been submitted.')
        return redirect('tourDetails',id=id)
    # Review already in database:
    if TourReviews.objects.filter(tour=tour,user=user).exists():
        review=TourReviews.objects.get(tour=tour,user=user)
        context['review']=review
        messages.add_message(request, messages.INFO, 'You have already submitted a review for this tour.')
    return render(request,"base/tourReview.html",context)

def teamProfile(request):
    context={}
    return render(request,"base/teamProfile.html",context)

# Delete review:
@login_required
def deleteTourReview(request,id):
    user=request.user
    tourId=NULL
    if TourReviews.objects.filter(id=id,user=user).exists():
        rev=TourReviews.objects.get(id=id,user=user)
        tourId=rev.tour.id
        rev.delete()
        messages.add_message(request, messages.INFO, 'You have successfully deleted your review.')
    return redirect('tourDetails',id=tourId)

def trip(request):
    context={}
    return render(request,"base/trip.html",context)

@login_required
def trips(request):
    savedTours=SavedTour.objects.filter(user=request.user)
    context={'savedTour':savedTours}
    return render(request,"base/trips.html",context)

@login_required
def userProfile(request):
    if request.method == 'POST':
        u_form =UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,request.FILES, instance=request.user.profile)          

        if u_form.is_valid() and p_form.is_valid():
            # Delete previous image from file system:
            prev_img=p_form.cleaned_data.get('image')
            profile=Profile.objects.get(user=request.user)
            if prev_img!=profile.image:
                profile.image.delete(save=False)
            u_form.save()
            p_form.save()
            messages.add_message(request, messages.SUCCESS, 'Your account has been Updated')
        else:
            messages.add_message(request, messages.ERROR, 'Please correct the error below.')
        return redirect('userProfile')
    else:
        u_form =UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context={
        'u_form':u_form,
        'p_form':p_form
    }
    return render(request, "base/userProfile.html",context)

# wishlist view function:
@csrf_exempt
@login_required
def userWishlist(request):
    user=request.user
    if request.method=='POST':
        body=json.loads(request.body.decode('utf-8'))
        id=body['id']
        wishlistDel=Wishlist.objects.get(id=id,user=user)
        wishlistDel.delete()
        return JsonResponse({'status':'success'})
    wishlist=Wishlist.objects.filter(user=user).order_by("-createadAt")
    context={
        'wishlist':wishlist
    }
    return render(request,"base/userWishlist.html",context)

@login_required
def updatePassword(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pass_form= PasswordChangingForm(user=request.user,data=request.POST)
            if pass_form.is_valid():
                pass_form.save()
                update_session_auth_hash(request , pass_form.user)
                messages.add_message(request, messages.SUCCESS, 'Your password has been updated successfully!')
                return redirect('userProfile')
        else:
            pass_form= PasswordChangingForm(user=request.user)

        context={
            'pass_form':pass_form
        }    
        return render(request,"base/updatePassword.html",context)
    else:
        return redirect('login')
       
# @login_required
def registerBusiness(request):
    if not request.user.is_authenticated:
        return redirect('login')
    id=request.GET.get('id')
    if id!=None:
        business=RegisteredBusiness.objects.get(id=id,user=request.user)
        context={'business':business}
    else:
        context={'business':None}
    if request.method=='POST' and id==None:
        name=request.POST.get('name')
        address=request.POST.get('address')
        zipcode=request.POST.get('zipcode')
        phone=request.POST.get('phone')
        email=request.POST.get('email')
        category=request.POST.get('category')
        website=request.POST.get('website')
        description=request.POST.get('description')
        lat=request.POST.get('latitude')
        lng=request.POST.get('longitude')
        logo=request.FILES.get('logo')
        banner=request.FILES.get('banner')
        business=RegisteredBusiness(user=request.user,name=name,address=address,zipcode=zipcode,phone=phone,email=email,category=category,description=description,lat=lat,lng=lng,logo=logo,banner=banner,website=website)
        business.save()
        html_content = render_to_string('base/email/email.html',{'title':'Your Business has been regisered','message':'Your Business has been regisered. Thank you.','name':name})
        text_content = strip_tags(html_content)
        email_content = EmailMultiAlternatives('Your Business has been registered successfully', text_content, settings.EMAIL_HOST_USER, [email])
        email_content.attach_alternative(html_content, "text/html")
        email_content.send()
        messages.add_message(request, messages.SUCCESS, 'Your Business has been registered successfully!')
        return redirect(f'/business/profile/?id={business.id}')
    if request.method=='POST' and id!=None:
        business=RegisteredBusiness.objects.get(id=id)
        business.name=request.POST.get('name')
        business.address=request.POST.get('address')
        business.zipcode=request.POST.get('zipcode')
        business.phone=request.POST.get('phone')
        business.email=request.POST.get('email')
        business.category=request.POST.get('category')
        business.website=request.POST.get('website')
        business.description=request.POST.get('description')
        business.lat=request.POST.get('latitude')
        business.lng=request.POST.get('longitude')
        if request.FILES.get('logo')!=None:
            # Delete the old logo from files system and save the new one:
            if business.logo!=None:
                business.logo.delete(save=False)
            business.logo=request.FILES.get('logo')
        if request.FILES.get('banner')!=None:
            # Delete the old banner from files system and save the new one:
            if business.banner!=None:
                business.banner.delete(save=False)
            business.banner=request.FILES.get('banner')
        business.save()
        context={'business':business}
        messages.add_message(request, messages.SUCCESS, 'Your Business has been updated successfully!')

    return render(request,"base/registerBusiness.html",context)

#Delete registered business:
@login_required
def deleteBusiness(request):
    id=request.GET.get('id')
    business=RegisteredBusiness.objects.get(id=id,user=request.user)
    context={'business':business}
    if request.method=='POST':
        business=RegisteredBusiness.objects.get(id=id)
        password=request.POST.get('password')
        if request.user.check_password(password):
            business.delete()
            # Send mail:
            html_content = render_to_string('base/email/email.html',{'title':'Your Business has been deleted','message':'Your Business has been deleted. Thank you.','name':business.name})
            text_content = strip_tags(html_content)
            email_content = EmailMultiAlternatives('Your Business has been deleted successfully', text_content, settings.EMAIL_HOST_USER, [business.email])
            email_content.attach_alternative(html_content, "text/html")
            email_content.send()
            messages.add_message(request, messages.SUCCESS, 'Your Business has been deleted successfully!')
            return redirect('home')
        else:
            messages.add_message(request, messages.ERROR, 'Please enter correct password!')
    return render(request,"base/deleteRegBiz.html",context)

# method to get nearby restaurants,hotels and repair shops:
@csrf_exempt
def getNearby(request,cat):
    nearbyVerified=[]
    nearbyUnverified=[]
    body=json.loads(request.body.decode('utf-8'))
    routeCoords=body['routeCoordinates']
    tourCoords=body['tourCoordinates']
    centerCoord=body['center']
    # Calculate radius of center:
    radius=10
    if len(tourCoords)>0:
        radius=haversine((centerCoord[0],centerCoord[1]),(tourCoords[0][0],tourCoords[0][1]))+3
    query1=RegisteredBusiness.objects.all().filter(category=cat)
    query2=Business.objects.all().filter(category=cat)

    locFiltered1=[loc for loc in query1 if haversine((loc.lat,loc.lng),(centerCoord[0],centerCoord[1]))<=radius]
    locFiltered2=[loc for loc in query2 if haversine((loc.lat,loc.lng),(centerCoord[0],centerCoord[1]))<=radius]
    if len(routeCoords)>0:
        for item in locFiltered1:
            for route in routeCoords:
                if haversine((item.lat,item.lng),(route["lat"],route["lng"]),unit=Unit.KILOMETERS)<=2:
                    nearbyVerified.append(item)
                    break
        for item in locFiltered2:
            for route in routeCoords:
                if haversine((item.lat,item.lng),(route["lat"],route["lng"]),unit=Unit.KILOMETERS)<=2:
                    nearbyUnverified.append(item)
                    break
    else:
        nearbyVerified=locFiltered1
        nearbyUnverified=locFiltered2
    querySer1=RegisteredBusinessSerializer(nearbyVerified,many=True)
    querySer2=BusinessSerializer(nearbyUnverified,many=True)
    data=querySer1.data+querySer2.data
    # data=serialize('json',nearby)
    return JsonResponse(data,safe=False)

# method to get recommendations:
@csrf_exempt
def getRecommendations(request,cat):
    body=json.loads(request.body.decode('utf-8'))
    tourCoords=body['tourCoordinates']
    centerCoord=body['center']
    # Calculate radius of center:
    radius=10
    if len(tourCoords)>0:
        radius=haversine((centerCoord[0],centerCoord[1]),(tourCoords[0][0],tourCoords[0][1]))+10
    query1=RegisteredBusiness.objects.all().filter(category=cat).order_by('-rating')
    query2=Business.objects.all().filter(category=cat).order_by('-rating')
    reco1=[loc for loc in query1 if haversine((loc.lat,loc.lng),(centerCoord[0],centerCoord[1]))<=radius]
    reco2=[loc for loc in query2 if haversine((loc.lat,loc.lng),(centerCoord[0],centerCoord[1]))<=radius]
    querySer1=RegisteredBusinessSerializer(reco1,many=True)
    querySer2=BusinessSerializer(reco2,many=True)
    data=querySer1.data+querySer2.data
    return JsonResponse(data,safe=False)

# method to get registered business by id
def getBusiness(request,id):
    business=RegisteredBusiness.objects.get(id=id)
    data=serialize('json',[business])
    return JsonResponse(data,safe=False)

# method to save tour to SaveTour table:
@login_required
@csrf_exempt
def saveTour(request):
    body=json.loads(request.body.decode('utf-8'))
    tourId=body['tourId']
    tourCoords=body['tourCoords']
    tourRoute=body['tourRoute']
    tour=Tour.objects.get(id=tourId)
    if SavedTour.objects.filter(tour=tour,user=request.user).exists():
        savedTour=SavedTour.objects.get(tour=tour,user=request.user)
        savedTour.tourCoords=tourCoords
        savedTour.tourRoute=tourRoute
        savedTour.save()
    else:
        saveTour=SavedTour(tour=tour,user=request.user,tourCoords=tourCoords,tourRoute=tourRoute)
        saveTour.save()
    return JsonResponse({"status":"success"},safe=False)

# method to delete saved tour:
@login_required
@csrf_exempt
def deleteSavedTour(request):
    body=json.loads(request.body.decode('utf-8'))
    id=body['id']
    savedTour=SavedTour.objects.get(id=id,user=request.user)
    savedTour.delete()
    return JsonResponse({"status":"success"},safe=False)

# method to handle a tour to wishlist:
@csrf_exempt
@login_required
def handleWishlist(request):
    body=json.loads(request.body.decode('utf-8'))
    tourId=body['tourId']
    option=body['option']
    tour=Tour.objects.get(id=tourId)
    user=request.user
    if option=='add':
        if Wishlist.objects.filter(user=user,tour=tour).exists():
            return JsonResponse({'status':'exists'})
        wishlist=Wishlist(user=user,tour=tour)
        wishlist.save()
        return JsonResponse({'status':'success'})
    if option=='remove':
        if Wishlist.objects.filter(user=user,tour=tour).exists():
            Wishlist.objects.get(user=user,tour=tour).delete()
        return JsonResponse({'status':'deleted'})
    
# Error page:
def error_404(request,exception):
    return render(request,'base/errorPages/404.html')

#delete user profile

def deleteUser(request,username,id):    
    profile = User.objects.get(username = username)
    context={'profile':profile}
    if request.method=='POST':
        profile=User.objects.get(id=id, email=request.user.email)
        userEmail=request.user.email
        password1=request.POST.get('password')
        if request.user.check_password(password1):
            # Clear user files:
            user_profile=Profile.objects.get(user=request.user)
            if user_profile.image != None:
                user_profile.image.delete(save=True)
            profile.delete()
            # Send mail:
            html_content = render_to_string('base/email/email.html',{'title':'Your account has been deleted','message':'Your account has been deleted successfully. Thank you.','username':User.username})
            text_content = strip_tags(html_content)
            email_content = EmailMultiAlternatives('Your account has been deleted successfully', text_content, settings.EMAIL_HOST_USER, [userEmail])
            email_content.attach_alternative(html_content, "text/html")
            email_content.send()
            messages.add_message(request, messages.SUCCESS, 'Your account has been deleted successfully!')
            return redirect('home')
        else:
            messages.add_message(request, messages.ERROR, 'Please enter correct password!')
    return render(request,"base/deleteUser.html",context)

def subscribe(request):
    if request.method=='POST':
        form=SubscribersForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Subscription Successful')
            return redirect('/subscribe')
    else:
        form=SubscribersForm()
    context={
        'form':form
    }
    return render(request,'base/subscribe.html',context)


def mail(request):
    emails=Subscribers.objects.all()
    df=read_frame(emails,fieldnames=['email'])
    mail_list=df['email'].values.tolist()
    if request.method=='POST':
       form=MailMessageForm(request.POST)
       if form.is_valid():
        form.save()
        title=form.cleaned_data.get('title')
        message=form.cleaned_data.get('message')
        send_mail(
        title,
        message,
        '',
        mail_list,
        fail_silently=False,
    )
        messages.success(request,"Your message has been sent successfully to the mail list!")
        return redirect('/mail')
    else:
        form=MailMessageForm()
    context={'form':form}
    return render(request,"base/mail.html",context)