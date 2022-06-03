from itertools import product
from unicodedata import category
from products.models import Products
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from accounts.forms import RegistrationForm
from accounts.models import Account
from twilio.rest import Client
import random
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    products= Products.objects.all().filter(is_available=True)
    # category= category.objects.all()
    context={
        'products':products,
        # 'category':category,
        }
    return render(request,'index.html',context)

def base(request):
    products= Products.objects.all().filter(is_available=True)
    # category= category.objects.all()
    context={
        'products':products,
        # 'category':category,
        }
    return render(request,'base.html',context)

def signin(request):
    if request.method == 'POST':
        email= request.POST['email']
        password= request.POST['password']
        # phone_number=Customer.objects.get('phone_number')
        user = authenticate(email=email,password=password)

        if user is not None:
            login(request,user)
            return render(request,'index.html')
        
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect('signin')
    return render(request,'signin.html')

def verification(request):
    if request.method == 'POST':
        phone_number= request.POST.get('phone_number')

        customer = Account.objects.filter(phone_number=phone_number)
        if not customer.exists():
            messages.info(request,'Phone number not registred, Kindly register')
            return redirect('register')

        account_sid="ACa03806fc4b0964cdfe06651f493789fa"
        auth_token="71136cbf562d9a504a273875e24366e6"
        client=Client(account_sid,auth_token)
        global otp
        otp = str(random.randint(1000,9999))
        message = client.messages.create(
                to= phone_number, 
                from_="+19595004778",
                body="Hello Your Login OTP is"+ otp )
        messages.success(request,'OTP has been sent to your phone number & enter OTP')
        return render (request, 'verification1.html')
    return render(request,'verification.html')

def verification1(request,id):
    if request.method=='POST':
        # phone_number= request.POST.get('phone_number')
        customer = Account.objects.get(id=id)
        otpvalue = request.POST['otp']
        # user = authenticate(id=customer)
        if otpvalue == otp:
            login(request,customer)
            messages.success(request,'You are logged in')
            return render (request, 'index.html')
            
        messages.error(request,'Invalid otp')
        return redirect('verification')
    return render(request, 'verification1.html')



def register(request):
    if request.method=='POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            first_name= form.cleaned_data['first_name']
            last_name= form.cleaned_data['last_name']
            email= form.cleaned_data['email']
            phone_number= form.cleaned_data['phone_number']
            password= form.cleaned_data['password']
            username=email.split("@")[0]
            user= Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,password=password,user_name=username)
            user.phone_number=phone_number
            user.save()
            messages.success(request,'Your account is created')
            return redirect('register')
        else:
            print(form.errors) 
    else:

        form = RegistrationForm()
    context = {
            'form':form
        }
    
    return render(request,'register.html',context)

def signout(request):
    
    if request.user.is_authenticated:
        logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('signin')

    
@login_required(login_url='signin')
def account_view(request):
     return render(request,'account_view.html')