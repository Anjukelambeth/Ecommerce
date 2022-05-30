from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from accounts.models import Account
from category.models import category
from products.models import Products
# from django.contrib.auth.decorators import user_passes_test
# Create your views here.


# @user_passes_test(lambda user: user.is_superuser)
def admin_panel(request):
    # admin_panel = user_passes_test(lambda u: u.is_superuser)(admin_panel)
    if request.method == 'POST':
    
        email= request.POST['email']
        password= request.POST['password']
        # phone_number=Customer.objects.get('phone_number')
        user = authenticate(email=email,password=password)

        if user is not None:
            login(request,user)
            return render(request,'admin_home.html')
        
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect('admin_panel')
    
    return render(request,'admin_signin.html')
# admin_panel = user_passes_test(lambda u: u.is_superuser)(admin_panel)   
def admin_home(request):
    return render(request,'admin_home.html')

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

def userblock(request):
    if request.user.is_authenticated:
        messages.info(request, "Are you really want to block this user!")
    return render(request,'block.html')
def userunblock(request):
    if request.user.is_authenticated:
        messages.info(request, "Are you really want to unblock this user!")
    return render(request,'unblock.html')

def admin_category(request):  
    if request.user.is_authenticated:
        categories = category.objects.all()
        return render(request,'admin_categoryview.html',{'category':categories})
    return redirect('admin_home')

def editcategory(request):
    pass
def add_category(request):
    pass


def deletecategory(request,id):  
    category = category.objects.get(id=id)  
    category.delete()  
    return redirect("/admin_categoryview")  

def admin_products(request):  
    if request.user.is_authenticated:
        product = Products.objects.all()
        return render(request,'admin_products.html',{'products':product})
    return redirect('admin_home')

def editproducts(request):
    pass

def deleteproducts(request,id):  
    category = category.objects.get(id=id)  
    category.delete()  
    return redirect("/admin_categoryview") 
    
def add_products(request):
    pass

