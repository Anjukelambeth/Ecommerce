from itertools import product
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from accounts.models import Account
from adminpanel.forms import OrderEditForm
from category.models import category
from orders.models import Order, OrderProduct
from products.models import Products
from category.forms import CategoryForm
from products.forms import ProductsForm
from django.contrib.auth.decorators import login_required
import os
from slugify import slugify
# from django.contrib.auth.decorators import user_passes_test
# Create your views here.



def admin_panel(request):
    if request.user.is_authenticated :
        return redirect('admin_panel')
    
    if request.method == 'POST':
        email= request.POST['email']
        password= request.POST['password']
        # phone_number=Customer.objects.get('phone_number')
        user = authenticate(request,email=email,password=password)

        if user is not None:
            if user.is_admin==True:
                login(request,user)
                return render(request,'admin_home.html')
            messages.error(request, "You are not permited to login!")
            return redirect('admin_panel')
        else:
            messages.warning(request, "Bad Credentials!!")
            return redirect('admin_panel')
    
    return render(request,'admin_signin.html')

@login_required(login_url='admin_panel')
def admin_home(request):
    return render(request,'admin_home.html')

@login_required(login_url='admin_panel')
def admin_signout(request):
    if request.user.is_authenticated:
        logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('admin_panel')

def admin_usersview(request):  
    if request.user.is_authenticated:
        users = Account.objects.all()
        return render(request,'admin_usersview.html',{'users':users})
    return redirect('admin_home')

# @login_required(login_url='admin_panel')
# # def userblock(request):
#     # if request.user.is_authenticated:
#     #     messages.warning(request, "Are you really want to block this user!?")
#     return render(request,'block.html')

@login_required(login_url='admin_panel')
def admin_userblock(request,id):
    user = Account.objects.get(id=id)
    user.is_active = False
    user.save()
    return redirect(admin_usersview)

@login_required(login_url='admin_panel')
def userunblock(request,id):
    user = Account.objects.get(id=id)
    user.is_active = True
    user.save()
    return redirect(admin_usersview)
    
def admin_category(request):  
    if request.user.is_authenticated:
        categories = category.objects.all()
        return render(request,'admin_categoryview.html',{'category':categories})
    return redirect('admin_home')

def edit_category(request,id):
    categorys = category.objects.get(id=id)
    form = CategoryForm(instance=categorys)
    if request.method =="POST":
        form = CategoryForm(request.POST or None, instance=categorys)
        if form.is_valid():  
            form.save()  
            messages.success(request,'Category updated successfully')
            return redirect('admin_category')
        else:
            print(form.errors)
    return render (request,'edit_category.html',{'form':form})

def add_category(request):
    form = CategoryForm(request.POST,request.FILES)
    if form.is_valid():
        form.save()
        messages.info(request,'Category added successfully')
        return redirect(admin_category)
    context ={
        'form':form
    }
    return render (request,'add_category.html',context)


def delete_category(request,id):  

    categori = category.objects.get(id=id)  
    categori.delete()  
    return redirect(admin_category)  

def admin_products(request):  
    if request.user.is_authenticated:
        product = Products.objects.all()
        return render(request,'admin_products.html',{'products':product})
    return redirect('admin_home')

def edit_products(request,id):
    product = Products.objects.get(id=id)
    form = ProductsForm(instance=product)
    if request.method =="POST":
        form = ProductsForm(request.POST or None,request.FILES, instance=product)
        if form.is_valid():  
            form.save()  
            messages.success(request,'Product updated successfully')
            return redirect(admin_products)
        else:
            print(form.errors)
    
    return render (request,'edit_products.html',{'form':form,'product':product})

# def edit_products(request,id):
#     product = Products.objects.get(id=id)
#     form = ProductsForm(instance=product)
#     if request.method =="POST":
#         form = ProductsForm(request.POST,request.FILES,instance=product)
#         if len(request.FILES)!=0:
#             if len(product.images)>0:
#                 os.remove(product.images.path)
#             product.images = request.FILES['images']
            
#             product.save()
#             messages.success(request,'Product edited successfully')
#             return redirect(admin_products)
        
#     return render (request,'edit_products.html',{'form':form,'product':product})


def delete_products(request,id):  
    product = Products.objects.get(id=id)  
    product.delete()  
    return redirect(admin_products) 
    
def add_products(request):
    # if request.method=='POST':
    form = ProductsForm(request.POST,request.FILES)
    if form.is_valid():
        form.save()
        messages.info(request,'Products added successfully')
        return redirect(admin_products)
    context ={
        'form':form
    }
    return render (request,'add_products.html',context)

def admin_order(request):
    orders = OrderProduct.objects.all()
    context = {
        'orders':orders,
        
    }
    return render (request,'admin_order.html',context)
    

def order_cancel(request,order_number):
    orders = Order.objects.get(order_number=order_number)
    orders.status ='Cancelled'
    orders.save()
    return redirect ('admin_order')

def admin_orderedit(request,order_number):
    orders = Order.objects.get(order_number=order_number)
    form = OrderEditForm(instance=orders)
    if request.method=='POST':
        form = OrderEditForm(request.POST)
        status = request.POST.get('status')
        orders.status = status
        orders.save()
        return redirect ('admin_order')
    context = {
        'orders':orders,
        'form':form
    }
    return render(request,'admin_orderedit.html',context)
