from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views
from .forms import UserPasswordResetForm,PasswordResetingForm

urlpatterns = [
    path('', views.home,name='home'),
    path('map/',views.map,name='map'),
    path('aboutUs/',views.aboutUs,name='aboutUs'),
    path('contact/',views.contact,name='contact'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('signup/',views.signup,name='signup'),
    path('recommendations/',views.recommendations,name='recommendations'),
    path('trip/',views.trip,name='trip'),
    path('trips/',views.trips,name='trips'),
    path('userProfile/',views.userProfile,name='userProfile'),
    path('tourForm/',views.tourForm,name='tourForm'),
    path('tourReview/<int:id>/',views.tourReview,name='tourReview'),
    path('registerBusiness/',views.registerBusiness,name='registerBusiness'),
    path('business/profile/',views.registerBusiness,name='businessProfile'),
    path('api/v1/tour/<int:id>',views.getTour,name='getTour'),
    path('api/v1/nearby/<str:cat>/',views.getNearby,name='getNearby'),
    path('api/v1/recommendations/<str:cat>/',views.getRecommendations,name='getRecommendations'),
    path('tourDetails/',views.tourDetails,name='tourDetails'),
    path('updatePassword/',views.updatePassword ,name='updatePassword'),
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name='base/passwordReset/password_reset_form.html', form_class=UserPasswordResetForm), name='reset_password'),
    path('reset_password/email/',auth_views.PasswordResetView.as_view(template_name='base/passwordReset/password_reset_form.html', form_class=UserPasswordResetForm, html_email_template_name='base/passwordReset/password_reset_email.html'), name='reset_password'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='base/passwordReset/password_reset_done.html') ,name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='base/passwordReset/password_reset_confirm.html', form_class=PasswordResetingForm) ,name='password_reset_confirm'),
    path('password_reset_complete',auth_views.PasswordResetCompleteView.as_view(template_name='base/passwordReset/password_reset_complete.html'),name='password_reset_complete'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)