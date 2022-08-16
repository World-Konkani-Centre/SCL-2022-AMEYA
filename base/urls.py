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
    path('subscribe/',views.subscribe,name='subscribe'),
    path('mail/',views.mail,name='mail'),
    path('trips/',views.trips,name='trips'),
    path('user/profile/',views.userProfile,name='userProfile'),
    path('team/',views.teamProfile,name='teamProfile'),
    path('user/profile/delete/<username>/<int:id>',views.deleteUser,name='delete_user'),
    path('user/wishlist',views.userWishlist,name='userWishlist'),
    path('tourForm/',views.tourForm,name='tourForm'),
    path('tour/review/<int:id>/',views.tourReview,name='tourReview'),
    path('tour/review/delete/<int:id>',views.deleteTourReview,name='deleteTourReview'),
    path('business/register/',views.registerBusiness,name='registerBusiness'),
    path('business/profile/',views.registerBusiness,name='profileBusiness'),
    path('business/delete/',views.deleteBusiness,name='deleteBusiness'),
    path('api/v1/tour/<int:id>',views.getTour,name='getTour'),
    path('api/v1/nearby/<str:cat>/',views.getNearby,name='getNearby'),
    path('api/v1/recommendations/<str:cat>/',views.getRecommendations,name='getRecommendations'),
    path('api/v1/tour/addToWishlist/',views.handleWishlist,name='handleWishlist'),
    path('tour/details/<int:id>',views.tourDetails,name='tourDetails'),
    path('updatePassword/',views.updatePassword ,name='updatePassword'),
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name='base/passwordReset/password_reset_form.html', form_class=UserPasswordResetForm), name='reset_password'),
    path('reset_password/email/',auth_views.PasswordResetView.as_view(template_name='base/passwordReset/password_reset_form.html', form_class=UserPasswordResetForm, html_email_template_name='base/passwordReset/password_reset_email.html'), name='reset_password'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='base/passwordReset/password_reset_done.html') ,name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='base/passwordReset/password_reset_confirm.html', form_class=PasswordResetingForm) ,name='password_reset_confirm'),
    path('password_reset_complete',auth_views.PasswordResetCompleteView.as_view(template_name='base/passwordReset/password_reset_complete.html'),name='password_reset_complete'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)