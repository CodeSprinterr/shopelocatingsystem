from django.urls import path
from . import views

urlpatterns =[
    path('',views.index,name='index'),
   
    
   
    
    path('about',views.about,name='about'),
    path('contactus',views.contactus,name='contactus'),
    
    
    
    path('registration',views.registration,name='registration'),
    path('profileupdate',views.profileupdate,name='profileupdate'),
   
    path('checkmail',views.checkmail,name='checkmail'),
    path('login',views.login,name='login'),
    path('forgotpassword',views.forgotpassword,name='forgotpassword'),
    path('operatorlogin',views.operatorlogin,name='operatorlogin'),
  
]


