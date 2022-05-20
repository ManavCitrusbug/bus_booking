"""bus_online_booking URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from bus import views
# from bus.views import Logout
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.Registerhome.as_view(),name='registerhome'),
    path('login/',views.Login.as_view(),name='login'),
    path('register/',views.Register.as_view(),name='register'),

    path('adminpage/',views.Admin.as_view(),name='adminpage'),
    path('createadmin/',views.Createadmin.as_view(),name='createadmin'),
    path('addbus/',views.Addbus.as_view(),name='addbus'),
    path('pessengerdetail/',views.Pessengerdetail.as_view(),name='pessengerdetail'),
    path('addbusdestination/',views.Addbusdestination.as_view(),name='addbusdestination'),
    path('delete/<int:id>/',views.Deletebus.as_view(),name='delete'),
    path('updatebus/<int:id>/',views.Editbus.as_view(),name='updatebus'),
    path('busbook/<int:id>/',views.Bookingbus.as_view(),name='busbook'),
    path('logout/',views.LogoutView.as_view(),name='logout'),
    path('busselect/',views.Userhome.as_view(),name='busselect'),
    path('userprofile/',views.Userprofile.as_view(),name='userprofile'),
    path('canclemessege/',views.Canclemessege.as_view(),name='canclemessege'),
    # path('canclebooking/',views.Canclebooking.as_view(),name='canclebooking'),
    path('cancleticket/',views.Cancleticket.as_view(),name='cancleticket'),
    path('deletepassenger/<int:id>/',views.Deletepessenger.as_view(),name='deletepassenger'),
   
    
  
    
]
