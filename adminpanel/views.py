from itertools import product
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from accounts.models import Account
from category.models import category
from products.models import Products
from category.forms import CategoryForm
from products.forms import ProductsForm
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.decorators import user_passes_test
# Create your views here.



def admin_panel(request):
    
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
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.info(request,'Category added successfully')
        return redirect(admin_category)
    context ={
        'form':form
    }
    return render (request,'add_category.html',context)


def deletecategory(request,id):  
    category = category.objects.get(id=id)  
    category.delete()  
    return redirect("/admin_categoryview")  

def admin_products(request):  
    if request.user.is_authenticated:
        product = Products.objects.all()
        return render(request,'admin_products.html',{'products':product})
    return redirect('admin_home')

def edit_products(request,id):
    product = Products.objects.get(id=id)
    form = ProductsForm(instance=product)
    if request.method =="POST":
        form = CategoryForm(request.POST or None, instance=product)
        if form.is_valid():  
            form.save()  
            messages.success(request,'Product updated successfully')
            return redirect('admin_category')
        else:
            print(form.errors)
    return render (request,'edit_category.html',{'form':form})


def deleteproducts(request,id):  
    category = category.objects.get(id=id)  
    category.delete()  
    return redirect("/admin_categoryview") 
    
def add_products(request):
    # if request.method=='POST':
    form = ProductsForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.info(request,'Products added successfully')
        return redirect(admin_products)
    context ={
        'form':form
    }
    return render (request,'add_products.html',context)

