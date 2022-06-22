import code
from django.core.paginator import Paginator
from inspect import modulesbyfile
from itertools import product
from multiprocessing import context
from category.models import category
from cart.models import Cart
from cart.views import _cart_id
from orders.models import Order, OrderProduct
from products.models import Products
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth import authenticate,login,logout
from accounts.forms import RegistrationForm,UserForm,AddAddressForm
from accounts.models import Account,UserAddresses,MyAccountManager
from twilio.rest import Client
import random
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    products= Products.objects.all().filter(is_available=True)
    categorys= category.objects.all()
    context={
        'products':products,
        'categorys':categorys,
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
        request.session['user_mobile'] = phone_number
        if not customer.exists():
            messages.info(request,'Phone number not registred, Kindly register')
            return redirect('register')

        account_sid="ACa03806fc4b0964cdfe06651f493789fa"
        auth_token="71136cbf562d9a504a273875e24366e6"
        client=Client(account_sid,auth_token)
        verification = client.verify \
                     .services("VAdf9ac283af0407b66228fa8b2d8e4fd0") \
                     .verifications \
                     .create(to=phone_number,channel='sms')
        print(verification.status)
        # message = client.messages.create(
        #         to= phone_number, 
        #         from_="+19595004778",
        #         body="Hello Your Login OTP is"+ otp )
        messages.success(request,'OTP has been sent to your phone number & enter OTP')
        return render (request, 'verification1.html')
    
    return render(request,'verification.html')

def verification1(request):
    if request.method=='POST':
        mobile_num= request.session['user_mobile']
    
        customer = Account.objects.filter(phone_number=mobile_num).first()
        otpvalue = request.POST['otp']
        # user = authenticate(id=customer)
        
        account_sid = "ACa03806fc4b0964cdfe06651f493789fa"
        auth_token = "71136cbf562d9a504a273875e24366e6"
        client = Client(account_sid, auth_token)
        verification_check = client.verify \
                                .services("VAdf9ac283af0407b66228fa8b2d8e4fd0") \
                                .verification_checks \
                                .create(to=mobile_num, code= otpvalue)
        # if otpvalue ==  otp:
        print(verification_check.status)
        if verification_check.status == "approved":
            auth.login(request,customer)
            try:
                del request.session['user_mobile']
                
            except:
                pass              
            
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

            request.session['user_email'] = email
            request.session['user_mobile'] = phone_number
            user= Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,password=password,phone_number=phone_number,user_name=username)
            user.save()

            account_sid="ACa03806fc4b0964cdfe06651f493789fa"
            auth_token="71136cbf562d9a504a273875e24366e6"
            client=Client(account_sid,auth_token)
            verification = client.verify \
                        .services("VAdf9ac283af0407b66228fa8b2d8e4fd0") \
                        .verifications \
                        .create(to=phone_number,channel='sms')
            print(verification.status)
            # messages.success(request,'Your account is created')
            messages.success(request,'OTP has been sent to your phone number & enter OTP')
            return redirect('verify_otp')
        else:
            print(form.errors) 
    else:

        form = RegistrationForm()
    context = {
            'form':form
        }
    
    return render(request,'register.html',context)

def verify_otp(request):
    if request.method == "POST":
        # generated_otp = request.POST['generated_otp']
        otp_input = request.POST['otp_input']
        user_mobile = request.session['user_mobile']
        user_email = request.session['user_email']        
        # print(user_mobile)   
        account_sid = "ACa03806fc4b0964cdfe06651f493789fa"
        auth_token = "71136cbf562d9a504a273875e24366e6"
        client = Client(account_sid, auth_token)
        
        verification_check = client.verify \
                                .services("VAdf9ac283af0407b66228fa8b2d8e4fd0") \
                                .verification_checks \
                                .create(to= user_mobile, code= otp_input)
    
        print(verification_check.status)
        if verification_check.status == "approved":
            messages.success(request,"OTP verified successfully.")
            user = Account.objects.get(email=user_email)
            user.is_active = True           
            user.save()          
            auth.login(request,user)          
            try:
                del request.session['user_mobile']
                del request.session['user_email']
            except:
                pass              
            
            # print('signing in')
            return redirect('index')
        else:
            messages.error(request,"Invalid OTP. Try again with correct OTP")
            return render(request,'login_otp.html')
    return render(request,'login_otp.html')


       

def signout(request):
    
    if request.user.is_authenticated:
        logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('signin')

    
@login_required(login_url='signin')
def account_view(request):
    profile = Account.objects.get(first_name=request.user.first_name)
    # orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id,is_ordered=True)
    orders = Order.objects.filter(user=request.user)
    orders_count=orders.count()
    context = {
        'profile':profile,
        'orders':orders, 
        'orders_count':orders_count
    }
    return render(request,'account_view.html',context)


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
    add=UserAddresses.objects.filter(user=request.user)
    if request.user.is_authenticated:            
        if request.method == "POST":
            # print("Got a POST request")
            form = AddAddressForm(request.POST)
            # print("checking the form validation")
            if form.is_valid():
                # print("Validation done collectiong, collecting data")
                user = Account.objects.get(id = request.user.id)
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                address_line_1 = form.cleaned_data['address_line_1']
                address_line_2 = form.cleaned_data['address_line_2']
                mobile = form.cleaned_data['mobile']
                email = form.cleaned_data['email']
                city = form.cleaned_data['city']
                state = form.cleaned_data['state']
                country = form.cleaned_data['country']
                zipcode= form.cleaned_data['zipcode']
                
                address = UserAddresses.objects.create(user=user,first_name=first_name,last_name=last_name,address_line_1=address_line_1,address_line_2=address_line_2, email=email, mobile=mobile, city=city, state=state, country=country, zipcode=zipcode)
                # print("going to save address")
                address.save()
                # print("address saved")       

                messages.success(request,"Your address has been registered. ")
                return redirect ('checkout')
        else:
            form = AddAddressForm()    
            context = {
                    'form':form,
                    'add':add,
            }
    # profile = get_object_or_404(UserAddresses,user=request.user)
    # if request.method =="POST":
    #     form = UserAddressForm(request.POST,instance=request.user)
    #     if form.is_valid():
    #         data=UserAddresses()
    #         data.user=request.user
    #         data.address_line_1= form.cleaned_data['address_line_1']
    #         data.address_line_2= form.cleaned_data['address_line_2']
    #         data.city= form.cleaned_data['city']
    #         data.zipcode= form.cleaned_data['zipcode']
    #         data.state= form.cleaned_data['state']
    #         user_address=UserAddresses.objects.create(address_line_1=data.address_line_1,address_line_2=data.address_line_2,city=data.city,zipcode=data.zipcode,state=data.state)
    #         user_address.save()
    #         form.save()
    #         data.save()
    #         messages.success(request,'Your profile has been updated')
    #         return redirect ('add_address')
    #     else:
    #         messages.info(request,'Unable to edit')
    # else:
    #     form = UserAddressForm(instance=request.user)
    #     add=UserAddresses.objects.filter(user=request.user)
            return render(request,'add_address.html',context)
    else:
        return redirect('signin')

def my_addresses(request):

    add = UserAddresses.objects.filter(user = request.user.id)
    context = {
        "add":add,
    }

    return render(request,'my_addresses.html',context)

def delete_address(request,add_id):
    # print(add_id)
    
    del_add = UserAddresses.objects.filter(user = request.user.id, id= add_id)

    del_add.delete()

    addresses = UserAddresses.objects.filter(user = request.user.id).order_by('-id')
    context = {
        "addresses":addresses,
    }
    return render(request,'accounts/my_addresses.html', context)

def edit_address(request,id):
    instance = get_object_or_404(UserAddresses, id=id)
    form = AddAddressForm(request.POST or None, instance=instance)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request,'Address has been updated')
            return redirect('my_addresses')
    else:  
        context = {
            'form'     : form,
            'address':instance,
            }
        return render(request, 'edit_address.html',context)
        
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
    
 
    # current_user = request.user
    
    orders = Order.objects.filter(user=request.user,is_ordered=True)
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

@login_required(login_url='login')
def order_detail(request,order_id):
    # print('order detail req recvd')
    order_detail = OrderProduct.objects.filter(order__order_number = order_id)
    order = Order.objects.get(order_number = order_id)
    # print('both details fetced')
    sub_total = 0
    for i in order_detail:
        sub_total += i.product_price * i.quantity
    context = {
        'order_detail':order_detail,
        'order':order,
        'sub_total': sub_total,
    }
    return render (request, 'order_detail.html',context)


def user_order_cancel(request,order_number):
    ord = Order.objects.get(order_number=order_number)
    ord.status='Cancelled'
    ord.save()
    return redirect('my_order')

def return_order(request,order_number):
    ord = Order.objects.get(order_number=order_number)
    ord.status='Returned'
    ord.save()
    return render (request,'order_return.html',{'ord':ord})