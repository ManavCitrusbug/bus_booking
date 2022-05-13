from asyncio import transports
from asyncio.trsock import TransportSocket
from email import message
import email
from multiprocessing import context
from tracemalloc import start
# from pyexpat.errors import messages
from django.contrib import messages

from unicodedata import category
from urllib import request
from django import views

from django.shortcuts import render,redirect

from django.http import HttpResponse,JsonResponse

from django.views import *
from datetime import datetime


from .models import *

from django.contrib.auth.models import User,auth
# from django.contrib.auth import *
class Login(View):

    def get(self,request):
        return render(request,'login.html')
    def post(self,request):
        un=request.POST['username']
        pwd=request.POST['password']
        user=auth.authenticate(username=un,password=pwd)
        
        

        if user is not None:
            
                if user.is_superuser:
                # Showbus.get(user)
                    auth.login(request,user)
                    return render(request,'admin.html')
                else:
                    auth.login(request,user)
                    return render(request,'userprofile.html')
        else:
            messages.info(request,'Invalid input')
            return redirect('login')

class Register(View):
    
    def get(self,request):
        return render(request,'register.html')

    def post(self,request):
        username=request.POST['username']
        firstname=request.POST['fn']
        lastname=request.POST['ln']
        Email=request.POST['email']
        pass1=request.POST['password']
        pass2=request.POST['confirmpassword']
        
        if User.objects.filter(username=username).exists():
            messages.info(request,'Username is Already Taken..')
            return redirect('register')
        elif User.objects.filter(email=Email).exists():
            messages.info(request,'Email is Already Taken..')
            return redirect('register')
     
        else:
                regi=User.objects.create_user(first_name=firstname,last_name=lastname,email=Email,password=pass1,username=username)
                regi.save()
                return redirect('register')

                




class Deletebus(View):
    
     def get(self,request,id):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                delet = Transport.objects.filter(pk=id)
                delet.delete()
                return redirect('adminpage')
            else:
                return redirect('login')
        else:
            return redirect('login')



class Bookingbus(View):
    def get(self,request,id):
        tran = Transport.objects.filter(pk=id)
        for t in tran:
            t1 = t.transport_name
          
        d=datetime.now()
        return render(request,'booked_bus.html',{'t1':t1, 'date':d})
    def post(self,request,id):
    
       
        bus=Transport.objects.get(transport_name=request.POST['bus'])
        # busid=Booked_bus.objects.get(pk=id)
        pessengername=request.POST['name']
        address=request.POST['address']
        phone=request.POST['phone']
        date=datetime.now()
        age=request.POST['age']
     
       
        busbooking=Booked_bus.objects.create(busname=bus,name=pessengername,address=address,phone=phone,book_date_time=date,age=age,user=request.user)
        busbooking.save()

        transport=Transport.objects.get(pk=id)
        busnumber=transport.number_plate
        price=transport.price_per_person
        context={'bus':bus,'pessengername':pessengername,'address':address,'phone':phone,'date':date,'age':age,'busnumber':busnumber,'price':price}

        return render(request,'ticketdetail.html',context)
        




        
        


class Admin(View):
    def get(self,request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                ts=Transport.objects.all()
                return render(request,'admin.html',{'transport':ts})
            # return render(request,'admin.html')
            else:
                return redirect('login')
        else:
            return redirect('login')

class Addbus(View):
    def get(self,request):
        if request.user.is_authenticated:
            if request.user.is_superuser == True:
                cat=Category.objects.all()
                return render(request,'add_bus.html',{'category':cat})
            else:
                return redirect('login')
        else:
            return redirect('login')
    def post(self,request):

            tn=request.POST['transport']
            busnumber=request.POST['busnumber']
          
            prz=request.POST['price']
            seats=request.POST['seat']
        
            ctgry=request.POST['category']
            category_object = Category.objects.get(category=ctgry)
            date_time=request.POST['date']
            if Transport.objects.filter(date_time_dpt=date_time).exists():
                if Transport.objects.filter(number_plate=busnumber).exists():
                    messages.info(request,'This Bus Are Already Exists in today Please Enter The New bus Number')
                    return redirect('addbus')
                else:
                    add=Transport.objects.create(transport_name=tn,number_plate=busnumber,seats_available=seats, price_per_person=prz,bus_category=category_object,date_time_dpt=date_time)
                    add.save()
                    return redirect('addbus')

            else:
                add=Transport.objects.create(transport_name=tn,number_plate=busnumber,seats_available=seats, price_per_person=prz,bus_category=category_object,date_time_dpt=date_time)
                add.save()
                return redirect('addbus')







class updatebus(View):
    def get(self,request,id):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                tran=Transport.objects.get(pk=id)
        
                def date(self, tran):
                    return tran.date_time_dpt.strftime('%Y-%m-%d')

                cat=Category.objects.all()
                return render(request,'updatebus.html',{'transport':tran,'category':cat, 'date':date})
            else:
                return redirect('login')
        else:
            return redirect('login')
    def post(self,request,id):
        tran = Transport.objects.get(pk=id)
        tran.transport_name=request.POST['transport']
        tran.number_plate=request.POST['busnumber']
        tran.seats_available=request.POST['seat']
        tran.price_per_person=request.POST['price']
        tran.bus_category = Category.objects.get(category= request.POST['category'])
        
        tran.date_time_dpt=request.POST['date']
       
        tran.save()
        return redirect('adminpage')

class LogoutView(View):
    def get(self, request):
        auth.logout(request)
        return redirect('login')

class Userhome(View):
    def get(self,request):
        
        if Transport.objects.all().exists():
            ts=Transport.objects.all()
            return render(request,'home.html',{'transport':ts})
        else:
            messages.info(request,'- - - - - - - - - - Sorry Bus Are not Available - - - - - - - - - -')
            return render(request,'home.html')
    def post(self,request):
        start = request.POST['start1']
        end = request.POST['end1']
        # end=request.POST['end_txt']
        date=request.POST['date1']
        journey=Journey.objects.filter(start_point=start, end_point=end)
       
        for i in journey:
            for j in i.transport.all():
                transport=Transport.objects.filter(date_time_dpt=date)
                print("********",transport)
                return render(request,'home.html',{'transport':transport})
                
        return JsonResponse({"a":'a'})


       

class Userprofile(View):
    def get(self,request):
        return render(request,'userprofile.html')

class Cancleboooking(View):

    def get(self,request):
        if request.user.is_authenticated:
     
                return render(request,'canclebooking.html')
   
        else:
            return redirect('login')   
    def post(self,request):
        phone=request.POST['phone']
        ph=Booked_bus.objects.filter(phone=phone) 
        if phone!='':  
            return render(request,'cancleticket.html',{'phn':ph})
        else:
            return redirect('cancleticket')

class Deletepessenger(View):
     def get(self,request,id):
        if request.user.is_authenticated: 
            if request.user.is_superuser:
                delet = Booked_bus.objects.get(pk=id)
                delet.delete()
                return render(request,'canclemessege.html')
            else:
                return redirect('login')
        else:
            return redirect('login')

class Canclemessege(View):
        def get(self,request):
            if request.user.is_authenticated:
                return render(request,'canclemessege.html')
            else:
                return redirect('login')
 
class Pessengerdetail(View):
        def get(self,request):
            if request.user.is_authenticated:
                detail=Booked_bus.objects.all()
                return render(request,'showpessenger.html',{'detail':detail})
            else:
                return redirect('login')
 
class Forgottenpassword(View):
        def get(self,request):
            Email=request.POST['email']
            if Email !='':
                if User.objects.get(email=Email).exists():
                    return render(request,'setnewpassword.html')
                else:
                    messages.info(request,'Email is not able')
                    return redirect('forgottenpassword')
            else:
                return redirect('forgottenpassword')



                
                
            

             
     
        



        





        

        


       


    

       
        


