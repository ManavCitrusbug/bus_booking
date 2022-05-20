from asyncio import transports
from asyncio.trsock import TransportSocket
from email import message
import email
from multiprocessing import context
from operator import add
from tracemalloc import start
# from pyexpat.errors import messages
from django.contrib import messages

from unicodedata import category
from urllib import request
from django import views

from django.shortcuts import render, redirect

from django.http import HttpResponse, JsonResponse

from django.views import *
from datetime import datetime


from .models import *

from django.contrib.auth.models import User, auth
# from django.contrib.auth import *


class Login(View):

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:

                if user.is_superuser:
                # Showbus.get(user)
                    auth.login(request, user)
                    return render(request, 'admin.html')
                else:
                    auth.login(request, user)
                    return render(request, 'userprofile.html')
        else:
            messages.info(request, 'Invalid input')
            return redirect('login')


class Register(View):

    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        username = request.POST['username']
        firstname = request.POST['fn']
        lastname = request.POST['ln']
        Email = request.POST['email']
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']

        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username is Already Taken..')
            return redirect('register')
        elif User.objects.filter(email=Email).exists():
            messages.info(request, 'Email is Already Taken..')
            return redirect('register')

        elif password == confirmpassword :
                regi = User.objects.create_user(
                    first_name=firstname, last_name=lastname, email=Email, password=password, username=username)
                regi.save()
                return redirect('register')
        else :
            return redirect('register')



class Deletebus(View):

     def get(self, request, id):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                deletebus = Transport.objects.filter(pk=id)
                deletebus.delete()
                return redirect('adminpage')
            else:
                return redirect('login')
        else:
            return redirect('login')


class Bookingbus(View):
    def get(self, request, id):
        transport = Transport.objects.filter(pk=id)
        for transports in transport:
            t1 = transports.transport_name

        d = datetime.now()
        return render(request, 'booked_bus.html', {'t1': t1, 'date': d})

    def post(self, request, id):

        bus = Transport.objects.get(transport_name=request.POST['bus'])
        # busid=Booked_bus.objects.get(pk=id)
        pessengername = request.POST['name']
        address = request.POST['address']
        phone = request.POST['phone']
        date = datetime.now()
        age = request.POST['age']

        busbooking = Booked_bus.objects.create(
            busname=bus, name=pessengername, address=address, phone=phone, book_date_time=date, age=age, user=request.user)
        busbooking.save()

        transport = Transport.objects.get(pk=id)
        busnumber = transport.number_plate
        price = transport.price_per_person
        context = {'bus': bus, 'pessengername': pessengername, 'address': address,
            'phone': phone, 'date': date, 'age': age, 'busnumber': busnumber, 'price': price}

        return render(request, 'ticketdetail.html', context)


class Admin(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                ts = Transport.objects.all()
                return render(request, 'admin.html', {'transport': ts})
            # return render(request,'admin.html')
            else:
                return redirect('login')
        else:
            return redirect('login')


class Addbus(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser == True:
                cat = Category.objects.all()

                return render(request, 'add_bus.html', {'category': cat})
            else:
                return redirect('login')
        else:
            return redirect('login')

    def post(self, request):

            tn = request.POST['transport']
            busnumber = request.POST['busnumber']

            price = request.POST['price']
            seats = request.POST['seat']

            category = request.POST['category']
            category_object = Category.objects.get(category=category)
            date_time = request.POST['date']
            if Transport.objects.filter(date_time_dpt=date_time).exists():
                if Transport.objects.filter(number_plate=busnumber).exists():
                    messages.info(
                        request, 'This Bus Are Already Exists in today Please Enter The New bus Number')
                    return redirect('addbus')
                else:
                    add = Transport.objects.create(transport_name=tn, number_plate=busnumber, seats_available=seats,
                                                   price_per_person=price, bus_category=category_object, date_time_dpt=date_time)
                    add.save()
                    return redirect('addbus')

            else:
                add = Transport.objects.create(transport_name=tn, number_plate=busnumber, seats_available=seats,
                                               price_per_person=price, bus_category=category_object, date_time_dpt=date_time)
                add.save()
                return redirect('addbus')


class Editbus(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                tran = Transport.objects.get(pk=id)

                def date(self, tran):
                    return tran.date_time_dpt.strftime('%Y-%m-%d')

                cat = Category.objects.all()
                return render(request, 'updatebus.html', {'transport': tran, 'category': cat, 'date': date})
            else:
                return redirect('login')
        else:
            return redirect('login')

    def post(self, request, id):
        tran = Transport.objects.get(pk=id)
        tran.transport_name = request.POST['transport']
        tran.number_plate = request.POST['busnumber']
        tran.seats_available = request.POST['seat']
        tran.price_per_person = request.POST['price']
        tran.bus_category = Category.objects.get(
            category=request.POST['category'])

        tran.date_time_dpt = request.POST['date']

        tran.save()
        return redirect('adminpage')


class LogoutView(View):
    def get(self, request):
        auth.logout(request)
        return redirect('login')


class Userhome(View):
    def get(self, request):
        if Transport.objects.all().exists():
            return render(request, 'home.html')
        else:
            messages.info(
                request, '- - - - - - - - - - Sorry Bus Are not Available - - - - - - - - - -')
            return render(request, 'home.html')

    def post(self, request):
        start = request.POST['start1']
        end = request.POST['end1']
        date = request.POST['date1']
     
        journey = Journey.objects.filter(start_point=start, end_point=end)
        for i in journey:
            date_filter = i.transport.filter(date_time_dpt=date)
            for j in date_filter:
                id = j.id
                name = j.transport_name
                number_plate = j.number_plate
                seats_available = j.seats_available
                price_per_person = j.price_per_person
                category = j.bus_category
                bus_category = category.category
                date_time_dpt = j.date_time_dpt
        return JsonResponse({"id":id, "name":name, "number_plate":number_plate, "seats_available":seats_available, "price_per_person":price_per_person, "date_time_dpt":date_time_dpt, "bus_category":bus_category})




class Userprofile(View):
    def get(self, request):
        return render(request, 'userprofile.html')







class Cancleticket(View):

    def get(self, request):
        if request.user.is_authenticated:

                return render(request, 'canclebooking.html')

        else:
            return redirect('login')

    def post(self, request):
        phone = request.POST['phone']
        ph = Booked_bus.objects.filter(phone=phone)
        if phone != '':
            if Booked_bus.objects.filter(phone=phone).exists():
                return render(request, 'cancleticket.html', {'phn': ph})
            else:
              
                return redirect('canclebooking')
        else:
            return redirect('canclebooking   ')


class Deletepessenger(View):
     def get(self, request, id):
        if request.user.is_authenticated:
                delet = Booked_bus.objects.get(pk=id)
                delet.delete()
                return render(request, 'canclemessege.html')
        else:
            return redirect('login')


class Canclemessege(View):
        def get(self, request):
            if request.user.is_authenticated:
                return render(request, 'canclemessege.html')
            else:
                return redirect('login')


class Pessengerdetail(View):
        def get(self, request):
            if request.user.is_authenticated:
                detail = Booked_bus.objects.all()
                return render(request, 'showpessenger.html', {'detail': detail})
            else:
                return redirect('login')


class Addbusdestination(View):
        def get(self, request):
            if request.user.is_authenticated:
                if request.user.is_superuser:
                    transport = Transport.objects.all()
                    return render(request, 'busdestination.html', {'transport': transport})
        def post(self,request):
            print('************',request.POST)
            if request.user.is_authenticated:
                if request.user.is_superuser:
                    startpoint=request.POST['start']
                    endpoint=request.POST['end']
                    ts=request.POST.getlist('destination')
                    print("************************",ts)
                    for i in ts:
                        # t = Transport.objects.filter(pk=i.id)
                        transport_object=Transport.objects.get(pk=i)
                        adddestination=Journey.objects.extend(start_point=startpoint,end_point=endpoint,transport=transport_object.transport_name)
                        adddestination.save()
                    return redirect('addbusdestination')
                else:
                        return redirect('login')
            else:
                        return redirect('login')
        

class Registerhome(View):
    def get(self,request):
        return render(request,'ragisterhome.html')


class Createadmin(View):
    def get(self, request):
      
                    return render(request, 'createadmin.html')

    def post(self, request):
        username = request.POST['username']
        firstname = request.POST['fn']
        lastname = request.POST['ln']
        Email = request.POST['email']
        pass1 = request.POST['password']
        # pass2 = request.POST['confirmpassword']
        # staff=request.POST['admin']
        # print('***********',staff)
        if User.objects.filter(username=username).exists():
            messages.info(request, 'This Admin Username is Already Taken..')
            return redirect('createadmin')
        elif User.objects.filter(email=Email).exists():
            messages.info(request, 'Email is Already Taken..')
            return redirect('createadmin')

        else:
                regi = User.objects.create_user(first_name=firstname, last_name=lastname, email=Email,
        password=pass1, username=username, is_staff=True, is_superuser=True)
                regi.save()
                return redirect('createadmin')




                         




                
                
            

             
     
        



        





        

        


       


    

       
        


