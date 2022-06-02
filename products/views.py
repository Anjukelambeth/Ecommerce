from category.models import category
from django.shortcuts import get_object_or_404, render,redirect
from .models import Products
from django.contrib import messages
# Create your views here.
def store(request,category_slug=None):
    categories=None
    products=None

    if category_slug != None:
        categories= get_object_or_404(category,slug=category_slug)
        products=Products.objects.filter(category=categories,is_available=True)
        product_count=products.count()
    else:
        products= Products.objects.all().filter(is_available=True)
        product_count=products.count()
    context= {
        'products':products,
        'product_count': product_count,
    }
    return render(request,'store.html',context)

def product_detail(request,category_slug,product_slug):
    try:
       single_product= Products.objects.get(category__slug=category_slug,slug=product_slug)
    except Exception as e:
        raise e
    context= {
        'single_product':single_product,
    }
    return render(request,'product_detail.html',context)
# def product_detail(request,cat_slug,prod_slug):
#     if(category.objects.filter(category_slug=cat_slug)):
#         if(Products.objects.filter(product_slug=prod_slug)):
#             product = Products.objects.filter(product_slug=prod_slug).first()
#             context = {'product':product}
    
#         else:
#             messages.error(request,'No such products')
#             return redirect('store')

#     else:
#         messages.error(request,'No such category')
#         return redirect('store')
#     return render(request, 'product_detail.html',context)
