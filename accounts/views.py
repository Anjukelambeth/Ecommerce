from inspect import modulesbyfile
from itertools import product
from multiprocessing import context
from re import U
from unicodedata import category
from cart.models import Cart
from cart.views import _cart_id
from orders.models import Order, OrderProduct
from products.models import Products
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth import authenticate,login,logout
from accounts.forms import RegistrationForm,UserForm,UserAddressForm
from accounts.models import Account,UserAddresses
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
    if request.user.is_authenticated :
        return redirect('signin')
    if request.method == 'POST':
        email= request.POST['email']
        password= request.POST['password']
        # phone_number=Customer.objects.get('phone_number')
        user = authenticate(email=email,password=password)

        if user is not None:
            try:
                cart=Cart.objects.get(cart_id=_cart_id(request))

            except:
                pass
            login(request,user)
            return render(request,'index.html')
        
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect('signin')
    return render(request,'signin.html')

def verification(request):
    if request.method == 'POST':
        phone_number= request.POST.get('phone_number')
        global mobile_num
        mobile_num=phone_number
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

def verification1(request):
    if request.method=='POST':
        # phone_number= Account.objects.get(phone_number=mobile_num)
    
        customer = Account.objects.filter(phone_number=mobile_num).first()
        otpvalue = request.POST['otp']
        # user = authenticate(id=customer)
        if otpvalue == otp:
            auth.login(request,customer)
            messages.success(request,'You are logged in')
            return render (request, 'index.html')
            
        messages.error(request,'Invalid otp')
        return redirect('verification')
    context={
        'customer':customer,
        'otpvalue':otpvalue,
    }
    return render(request, 'verification1.html',context)



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


def user_profile(request):
    profile = Account.objects.get(first_name=request.user.first_name)
    
    context = {
        'profile':profile
    }
    return render(request,'user_profile.html',context)

#profile edit
@login_required(login_url='signin')
def user_profile_edit(request):
    # profile = get_object_or_404(Account,user=request.user)
    # form = RegistrationForm(instance=profile)
    if request.method =="POST":
        user_form = UserForm(request.POST,instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request,'Your profile has been updated')
            return redirect ('user_profile_edit')
        else:
            messages.info(request,'Unable to edit')
    else:
        user_form = UserForm(instance=request.user)
    return render(request,'user_profile_edit.html',{'form':user_form,'profile':request.user})

@login_required(login_url='signin')
def add_address(request):
    # profile = get_object_or_404(UserAddresses,user=request.user)
    if request.method =="POST":
        form = UserAddressForm(request.POST,instance=request.user)
        if form.is_valid():
            data=UserAddresses()
            data.user=request.user
            data.address_line_1= form.cleaned_data['address_line_1']
            data.address_line_2= form.cleaned_data['address_line_2']
            data.city= form.cleaned_data['city']
            data.zipcode= form.cleaned_data['zipcode']
            data.state= form.cleaned_data['state']
            user_address=UserAddresses.objects.create(address_line_1=data.address_line_1,address_line_2=data.address_line_2,city=data.city,zipcode=data.zipcode,state=data.state)
            user_address.save()
            form.save()
            data.save()
            messages.success(request,'Your profile has been updated')
            return redirect ('add_address')
        else:
            messages.info(request,'Unable to edit')
    else:
        form = UserAddressForm(instance=request.user)
    # add=UserAddresses.objects.filter(user=request.user)
    return render(request,'add_address.html',{'form':form,'profile':request.user})

@login_required(login_url='signin')
def change_password(request):
    if request.method == 'POST':
        current_password=request.POST['current_password']
        new_password=request.POST['new_password']
        confirm_password=request.POST['confirm_password']

        user=Account.objects.get(user_name__exact=request.user.user_name)

        if new_password==confirm_password:
            success =user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request,'Your password has been updated')
                return redirect ('change_password')
            else:
                messages.error(request,'Please enter valid current password')
                return redirect ('change_password')
        else:
            messages.error(request,'Password is not match')
            return redirect ('change_password')
    return render(request,'change_password.html')

def my_order(request):
    current_user = request.user
    orders = Order.objects.filter(user=current_user)
    context ={
        'orders':orders, 
    }
    return render(request,'my_order.html',context)
@login_required(login_url='signin')
def order_view(request,order_id):
    # ord = Order.objects.filter(order_number=id).filter(user=request.user).first()
    # orders = OrderProduct.objects.filter(order=ord)
    order_view=OrderProduct.objects.filter(order__order_number=order_id)
    order=Order.objects.get(order_number=order_id)
    context ={
        # 'orders':orders,
        # 'ord':ord,
        'order_view':order_view,
        'order':order,
    }
    return render(request,'order_view.html',context)


def user_order_cancel(request,order_number):
    ord = Order.objects.get(order_number=order_number)
    ord.status='Cancelled'
    ord.save()
    return redirect('my_order')