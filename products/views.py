from ast import keyword
from itertools import product
from multiprocessing import context
from django.http import HttpResponse, JsonResponse
from category.models import category
from django.shortcuts import get_object_or_404, render,redirect
from django.db.models import Q
from products.models import Products
from django.template.loader import render_to_string
from .models import Products
from django.contrib import messages
from cart.models import CartItem
from cart.views import _cart_id
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
# Create your views here.
def store(request,category_slug=None):
    categories=None
    products=None

    price = request.GET.get('price', "")

    if category_slug != None:
        categories = get_object_or_404(category, slug=category_slug)
        products = Products.objects.filter(category= categories, is_available=True).order_by('product_name')
        total_count = Products.objects.all().filter(is_available=True).order_by('product_name').count()


        # filter by 
        filter_by = request.GET.get("price") 
        if filter_by == "500":  
             products = Products.objects.all().filter(price__lte=500).order_by('-price')
        elif filter_by == "1000":  
             products = Products.objects.all().filter(price__lte=1000).order_by('-price')
        elif filter_by == "5000":  
             products = Products.objects.all().filter(price__lte=5000).order_by('-price')
        elif filter_by == "10000":  
             products = Products.objects.all().filter(price__lte=10000).order_by('-price')

        
        

        p = Paginator(products, 4)
        page = request.GET.get('page')
        page_products = p.get_page(page)
        product_count = products.count()         

    else:
        products = Products.objects.all().filter(is_available=True).order_by('product_name')
        total_count = Products.objects.all().filter(is_available=True).order_by('product_name').count()

        # filter by 
        filter_by = request.GET.get("price") 
        if filter_by == "500":  
             products = Products.objects.all().filter(price__lte=500).order_by('-price')
        elif filter_by == "1000":  
             products = Products.objects.all().filter(price__lte=1000).order_by('-price')
        elif filter_by == "5000":  
             products = Products.objects.all().filter(price__lte=5000).order_by('-price')
        elif filter_by == "10000":  
             products = Products.objects.all().filter(price__lte=10000).order_by('-price')
        
        

        p = Paginator(products, 4)
        page = request.GET.get('page')
        page_products = p.get_page(page)
        product_count = products.count()    

        

    context = { 
        'products' : page_products,
        'product_count' : product_count,
        'total_count' : total_count,

        }
   
    
    return render(request,'store.html',context)

def product_detail(request,category_slug,product_slug):
    try:
       single_product= Products.objects.get(category__slug=category_slug,slug=product_slug)
       in_cart=CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
    except Exception as e:
        raise e
    context= {
        'single_product':single_product,
        'in_cart': in_cart,
    }
    return render(request,'product_detail.html',context)

def search(request):
    if 'keyword' in request.GET:
        keyword= request.GET['keyword']
        if keyword:
            products=Products.objects.order_by('-created_date').filter(Q(product_description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count=products.count()
        context={
            'products':products,
            'product_count':product_count,
        }
    return render(request,'store.html',context)

