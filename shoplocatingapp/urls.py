from django.urls import path
from . import views

urlpatterns =[
    path('',views.index,name='index'),
    path('searchbyarea',views.searchbyarea,name='searchbyarea'),   
    path('state',views.state,name='state'),
    path('district',views.district,name='district'),
    path('citylist',views.citylist,name='citylist'),
    path('arealist',views.arealist,name='arealist'),
    path('displayshop',views.displayshop,name='displayshop'),
    
    path('getlocation', views.getlocation ,name = "getlocation"),
    path('itemlist', views.itemlist ,name = "itemlist"),
    path('searchbyitem',views.searchbyitem,name='searchbyitem'),  
    path('searchbyshop',views.searchbyshop,name='searchbyshop'),  
    path('getshopname',views.getshopname,name='getshopname'),
    
    path('about',views.about,name='about'),
    path('contactus',views.contactus,name='contactus'),
    
    
    path('additem',views.additem,name='additem'),
    path('itemdelete',views.itemdelete,name='itemdelete'),
    path('itemdeletelist',views.itemdeletelist,name='itemdeletelist'),
    path('header',views.header,name='header'),
    path('footer',views.footer,name='footer'),
    path('itemupdate',views.itemupdate,name='itemupdate'),
    path('itemupdatelist',views.itemupdatelist,name='itemupdatelist'),
    path('header',views.header,name='header'),
    path('footer',views.footer,name='footer'),
    path('registration',views.registration,name='registration'),
    path('profileupdate',views.profileupdate,name='profileupdate'),
   
    path('checkmail',views.checkmail,name='checkmail'),
    path('login',views.login,name='login'),
    path('forgotpassword',views.forgotpassword,name='forgotpassword'),
    path('operatorlogin',views.operatorlogin,name='operatorlogin'),
    path('home',views.home,name='home'),
    path('addlocation',views.addlocation,name='addlocation'),
    path('header1',views.header1,name='header1'),
]


