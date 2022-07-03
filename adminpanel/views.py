import calendar
from itertools import product
from multiprocessing import context
from django.http import FileResponse, HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from accounts.models import Account
from adminpanel.filters import FilterAccount, FilterCategory, FilterOrder, FilterProducts
from adminpanel.forms import CategoryOfferForm, OrderEditForm, ProductOfferForm
from adminpanel.models import CategoryOffer, ProductOffer
from category.models import category
from coupons.forms import CouponApplyForm
from coupons.models import Coupon
from orders.forms import OrderStatusForm
from orders.models import Order, OrderProduct
from products.models import Products, Variation
from category.forms import CategoryForm
from products.forms import ProductsForm, VariationForm
from django.contrib.auth.decorators import login_required
import os
from dateutil.relativedelta import relativedelta
from datetime import date,datetime,timedelta
from django.utils.text import Truncator
from django.db.models.functions import TruncDate, TruncDay, TruncMonth, TruncWeek
from django.views.decorators.cache import cache_control
from slugify import slugify
from django.db.models.functions import ExtractMonth,ExtractDay
from django.db.models import Count,Sum
import csv
from csv import writer
from datetime import datetime
# from weasyprint import HTML, html
import tempfile
from django.template.loader import render_to_string
# import os
import xlwt
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from django.core.paginator import Paginator
from reportlab.lib.pagesizes import letter

from refferalcode.forms import RefferalApplyForm
from refferalcode.models import Refferal
# os.add_dll_directory()
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
    #ORDER GRAPH
    orderbyday = Order.objects.annotate(day=ExtractDay('created_at')).values('day').annotate(count=Count('id'))
    print(orderbyday)
    dayday =[]
    orderperday =[]
    for o in orderbyday:
        dayday.append(o['day'])
        orderperday.append(o['count'])
    order = Order.objects.annotate(month=ExtractMonth('created_at')).values('month').annotate(count=Count('id')).values('month','count')
    monthNumber = []
    totalOrder = []
    for ord in order:
        monthNumber.append(calendar.month_name[ord['month']])
        totalOrder.append(ord['count'])
    #total users
    users_count = Account.objects.all().count()

    #total revenue
    revenue=0
    order = OrderProduct.objects.all()
    for item in order:
        revenue = revenue + item.product_price

    #total order
    order_count = Order.objects.all().count()

    
    # order_status = Order.objects.annotate(status=Value(Ac)).values('statu').annotate(count=Count('id'))
    # status_status =[]
    # status_count =[]
    
    # print(order_status)
    completed_order = Order.objects.filter(status='Completed').count()
    pending_order = Order.objects.filter(status='New').count()
    accepted_order = Order.objects.filter(status='Accepted').count()
    order_status_list = []
    order_status_list.append(completed_order)
    order_status_list.append(accepted_order)
    order_status_list.append(pending_order)
    print(order_status_list)

    context = {
        'monthNumber':monthNumber,
        'totalOrder':totalOrder,
        'dayday':dayday,
        'orderperday':orderperday,
        'users_count':users_count,
        'revenue':revenue,
        'order_count':order_count,
        'order_status_list':order_status_list,
        # 'today_revenue':today_revenue,
        }
    
    return render(request,'admin_home.html',context)

#csv export
def export_csv(request):
    response = HttpResponse(content_type='text/csf')
    response['Content-Disposition']='attachement; filename=Expenses' + str(datetime.now())+'.csv'
    writer = csv.writer(response)
    writer.writerow(['Amount','name','date','order'])
    orders = Order.objects.filter(status='Completed')
    for i in orders:
        writer.writerow([i.first_name])
    return response

#excel export 
def export_excel(request):
    response = HttpResponse(content_type='applications/ms-excel')
    response['Content-Disposition']='attachement; filename=Expenses' + str(datetime.now())+'.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws =wb.add_sheet('Expenses')
    row_num=0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['first_name','last_name','order_number','status']
    for col_num in range(len(columns)):
        ws.write(row_num,col_num,columns[col_num],font_style)
    font_style = xlwt.XFStyle()
    
    rows = Order.objects.all().values_list('first_name','last_name','order_number','status')
    for row in rows:
        row_num+=1

        for col_num in range(len(row)):
            ws.write(row_num,col_num,str(row[col_num]),font_style)
    wb.save(response)
    return response

#export to pdf
# def export_pdf(request):
#     response = HttpResponse(content_type='applications/pdf')
#     response['Content-Disposition']='attachement; inline; filename=Expenses' + str(datetime.now())+'.pdf'
#     response['Content-Transfer-Encoding']='binary'
#     orders = Order.objects.all()
#     context ={
#         'orders':orders,

#     }
#     html_string = render_to_string('admin_panel/pdf_output.html',context)
#     html = HTML(string=html_string)
#     result = html.write_pdf()


#     with tempfile.NamedTemporaryFile(delete=True) as output: 
#         output.write(result)
#         output.flush()

#         output = open(output.name,'rb')
#         response.write(output.read())
#     return response


@login_required(login_url='admin_panel')
def admin_signout(request):
    if request.user.is_authenticated:
        logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('admin_panel')

@login_required(login_url='admin_panel')
def admin_usersview(request):  
    # if request.user.is_authenticated:
    users = Account.objects.all()
    filters = FilterAccount(request.GET, queryset=users)
    users=filters.qs
    context={
        'users':users,
        'filters':filters,
    }
    return render(request,'admin_usersview.html',context)
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

@login_required(login_url='admin_panel')    
def admin_category(request):  
    # if request.user.is_authenticated:
    categories = category.objects.all()
    filters = FilterCategory(request.GET, queryset=categories)
    categories=filters.qs
    context={
        'category':categories,
        'filters':filters,
    }
    return render(request,'admin_categoryview.html',context)
    return redirect('admin_home')

@login_required(login_url='admin_panel')
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

@login_required(login_url='admin_panel')
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

@login_required(login_url='admin_panel')
def delete_category(request,id):  

    categori = category.objects.get(id=id)  
    categori.delete()  
    return redirect(admin_category)  

@login_required(login_url='admin_panel')
def admin_products(request): 
    product = Products.objects.all() 
    filters = FilterProducts(request.GET, queryset=product) 
    # if request.user.is_authenticated:
    #     product = Products.objects.all() 
	    

	    
    return render(request,'admin_products.html',{'filters':filters})
    return redirect('admin_home')

@login_required(login_url='admin_panel')
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

@login_required(login_url='admin_panel')
def delete_products(request,id):  
    product = Products.objects.get(id=id)  
    product.delete()  
    return redirect(admin_products) 

@login_required(login_url='admin_panel')    
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

@login_required(login_url='admin_panel')
def admin_variation_table(request):
    variation = Variation.objects.all()
    
    context = {
        'variation':variation,
        
    }
    return render (request,'admin_variation.html',context)

@login_required(login_url='admin_panel')
def admin_order(request):
    orders = OrderProduct.objects.all()
  
    filters = FilterOrder(request.GET, queryset=orders)
    orders=filters.qs

    # paginator = Paginator(orderss, 15) # Show 25 contacts per page.
    # page_number = request.GET.get('page')
    # orders = paginator.get_page(page_number)

    context = {
        'orders':orders,
        'filters':filters,
    }
    return render (request,'admin_order.html',context)


@login_required(login_url='admin_panel')
def order_cancel(request,order_number):
    orders = Order.objects.get(order_number=order_number)
    orders.status ='Cancelled'
    orders.save()
    return redirect ('admin_order')

@login_required(login_url='admin_panel')
def cancel_order_admin(request, order_number):
    order = Order.objects.get( order_number= order_number)
    order.status = 'Cancelled'
    order.save()
    
    return redirect('order')

@login_required(login_url='admin_panel')    
def return_order_admin(request, order_number):
    order = Order.objects.get( order_number= order_number)
    order.status = 'Returned'
    order.save()
    
    return redirect('order')

@login_required(login_url='admin_panel')
def deliver_order(request, order_number):
    order = Order.objects.get( order_number= order_number)
    order.status = 'Delivered'
    order.save()
    
    return redirect('order')

@login_required(login_url='admin_panel')
def ship_order(request, order_number):
    order = Order.objects.get( order_number= order_number)
    order.status = 'Shipped'
    order.save()
    
    return redirect('order')

@login_required(login_url='admin_panel')
def order_order(request, order_number):
    order = Order.objects.get( order_number= order_number)
    order.status = 'Ordered'
    order.save()
    
    return redirect('order')

@login_required(login_url='admin_panel')
def admin_orderedit(request,order_number):
    
    instance = get_object_or_404(Order, order_number = order_number)

    form = OrderStatusForm(request.POST or None, instance=instance)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request,'Order Status has been updated')
            return redirect('admin_order')
    else:  
        context = {
            'form'     : form,
            'order': instance,
            }
    # orders = Order.objects.get(order_number=order_number)
    # form = OrderEditForm(instance=orders)
    # if request.method=='POST':
    #     form = OrderEditForm(request.POST)
    #     status = request.POST.get('status')
    #     orders.status = status
    #     orders.save()
    #     return redirect ('admin_order')
    # context = {
    #     'orders':orders,
    #     'form':form
    # }
        return render(request,'admin_orderedit.html',context)

@login_required(login_url='admin_panel')
def admin_offerview(request):
    coupon_offers = Coupon.objects.all().order_by('-valid_to')
    # refferal_offers = Coupon.objects.all().order_by('-valid_to')
    prod_offers = ProductOffer.objects.all().order_by('-valid_to')
    cat_offers = CategoryOffer.objects.all().order_by('-valid_to')


    paginator = Paginator(coupon_offers, 5) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    context = {
        'coupon_offers': page_obj,
        'prod_offers': prod_offers,
        'cat_offers': cat_offers,
        # 'refferal_offers': refferal_offers,

    }
    
    # product_offer = ProductOffer.objects.all()
    
    # context={
       
    #     'product_offer':product_offer,
        
    # }
    return render (request,'offer_view.html',context)

# OFFERS SECTION

# coupon offers
@login_required(login_url='admin_login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_coupon(request):
    form = CouponApplyForm(request.POST or None, request.FILES or None)  
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('admin_offerview')
        else:
            messages.error(request,'form not valid')            
            context = {
            'form':form
            }
            return render(request,'add_coupon.html',context)
    else:
        context = {
            'form':form
        }
        return render(request,'add_coupon.html',context)
    
    
    
@login_required(login_url='admin_login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_coupon(request,c_id):
    instance = get_object_or_404(Coupon, id=c_id)
    form = CouponApplyForm(request.POST or None, instance=instance)


    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request,'Product has been updated')
            return redirect('admin_offerview')
        else:
             context = {
            'form'     : form,
            'coupon':instance,
            }
        return render(request, 'edit_coupon_offer.html',context)
    else:  
        context = {
            'form'     : form,
            'coupon':instance,
            }
        return render(request, 'edit_coupon_offer.html',context)
    

@login_required(login_url='admin_login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def activate_coupon(request):
    coupon_id = request.GET['couponId']
    coupon = Coupon.objects.get(id = coupon_id)
    coupon.active = True
    coupon.save()

    return redirect('admin_offerview')


@login_required(login_url='admin_login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def block_coupon(request):
  
    coupon_id = request.GET['couponId']
    coupon = Coupon.objects.get(id = coupon_id)
    coupon.active = False
    coupon.save()

    return redirect('admin_offerview')



@login_required(login_url='admin_login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_coupon(request):
    coupon_id = request.GET['couponId']
    coupon = Coupon.objects.get(id = coupon_id)
    
    coupon.delete()

    return redirect('admin_offerview')

# refferal offers
# @login_required(login_url='admin_login')
# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# def add_refferal(request):
#     form = RefferalApplyForm(request.POST or None, request.FILES or None)  
#     if request.method == "POST":
#         if form.is_valid():
#             form.save()
#             return redirect('admin_offerview')
#         else:
#             messages.error(request,'form not valid')            
#             context = {
#             'form':form
#             }
#             return render(request,'add_refferal.html',context)
#     else:
#         context = {
#             'form':form
#         }
#         return render(request,'add_refferal.html',context)
    
    
    
# @login_required(login_url='admin_login')
# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# def edit_refferal(request,c_id):
#     instance = get_object_or_404(Refferal, id=c_id)
#     form = RefferalApplyForm(request.POST or None, instance=instance)


#     if request.method == "POST":
#         if form.is_valid():
#             form.save()
#             messages.success(request,'Code has been updated')
#             return redirect('admin_offerview')
#         else:
#              context = {
#             'form'     : form,
#             'coupon':instance,
#             }
#         return render(request, 'edit_refferal.html',context)
#     else:  
#         context = {
#             'form'     : form,
#             'coupon':instance,
#             }
#         return render(request, 'edit_refferal.html',context)
    

# @login_required(login_url='admin_login')
# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# def activate_refferal(request):
#     coupon_id = request.GET['couponId']
#     coupon = Refferal.objects.get(id = coupon_id)
#     coupon.active = True
#     coupon.save()

#     return redirect('admin_offerview')


# @login_required(login_url='admin_login')
# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# def block_refferal(request):
  
#     coupon_id = request.GET['couponId']
#     coupon = Refferal.objects.get(id = coupon_id)
#     coupon.active = False
#     coupon.save()

#     return redirect('admin_offerview')



# @login_required(login_url='admin_login')
# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# def delete_refferal(request):
#     coupon_id = request.GET['couponId']
#     coupon = Refferal.objects.get(id = coupon_id)
    
#     coupon.delete()

#     return redirect('admin_offerview')


@login_required(login_url='admin_panel')
def add_product_offer(request):
    form = ProductOfferForm(request.POST  or None, request.FILES or None)
    print("product offer")
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.info(request,'Product offer added successfully')
            return redirect(admin_offerview)
        else:
            messages.error(request,'form not valid')   
            context ={
                    'form':form
             } 
            return render (request,'add_product_offer.html',context)
    else:
        context ={
            'form':form
        }
        return render (request,'add_product_offer.html',context)

#product offer edit
@login_required(login_url='admin_panel')
def edit_product_offer(request,id):
    offer = ProductOffer.objects.get(id=id)
    form = ProductOfferForm(instance=offer)
    if request.method =="POST":
        form = ProductOfferForm(request.POST,instance=offer)
        form.save()
        messages.success(request,'Product offer updated successfully')
        return redirect('admin_offerview')
    return render (request,'edit_product_offer.html',{'form':form,'offer':offer})

@login_required(login_url='admin_login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def activate_product_offer(request):
    offer_id = request.GET['proOffId']
   
    offer = ProductOffer.objects.get(id = offer_id)

    offer.is_active = True
    offer.save()

    return redirect('admin_offerview')


@login_required(login_url='admin_login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def block_product_offer(request):
    offer_id = request.GET['proOffId']
    offer = ProductOffer.objects.get(id = offer_id)
    offer.is_active = False
    offer.save()

    return redirect('admin_offerview')

@login_required(login_url='admin_login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_product_offer(request):
    offer_id = request.GET['proOffId']
    offer = ProductOffer.objects.get(id = offer_id)
    
    offer.delete()

    return redirect('admin_offerview')



# def delete_product_offer(request,id):
#     offer = ProductOffer.objects.get(id=id)
#     offer.delete()
#     return redirect(admin_offerview)

@login_required(login_url='admin_login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_cat_offer(request):

    form = CategoryOfferForm(request.POST or None, request.FILES or None)  
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('admin_offerview')
        else:
            messages.error(request,'form not valid')            
            context = {
            'form':form
            }
            return render(request,'add_cat_offer.html',context)
    else:
        context = {
            'form':form
        }
        return render(request,'add_cat_offer.html',context)

@login_required(login_url='admin_login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_cat_offer(request,cat_id):
    instance = get_object_or_404(CategoryOffer, id=cat_id)
    form = CategoryOfferForm(request.POST or None, instance=instance)
  

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request,'Offer has been updated')
            return redirect('admin_offerview')
        else:
             context = {
            'form'     : form,
            'coupon':instance,
            }
        return render(request, 'edit_cat_offer.html',context)
    else:  
        context = {
            'form'     : form,
            'coupon':instance,
            }
        return render(request, 'edit_cat_offer.html',context)


@login_required(login_url='admin_login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def activate_cat_offer(request):
    offer_id = request.GET['catOffId']
    
    offer = CategoryOffer.objects.get(id = offer_id)
 
    offer.is_active = True
    offer.save()

    return redirect('admin_offers')


@login_required(login_url='admin_login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def block_cat_offer(request):
    offer_id = request.GET['catOffId']
    offer = CategoryOffer.objects.get(id = offer_id)
    offer.is_active = False
    offer.save()

    return redirect('admin_offerview')


@login_required(login_url='admin_login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_cat_offer(request):
    offer_id = request.GET['catOffId']
    offer = CategoryOffer.objects.get(id = offer_id)
    
    offer.delete()

    return redirect('admin_offerview')

@login_required(login_url='admin_panel')
def report_pdf(request):
    # create  bytestream buffer
    buf = io.BytesIO()
    # create a canvas
    cnvs = canvas.Canvas(buf, pagesize=letter, bottomup= 0)
    # create a text object
    textobj = cnvs.beginText()
    textobj.setTextOrigin(inch, inch)
    textobj.setFont("Helvetica", 14)
    
    orders = OrderProduct.objects.all()
    lines = []

    for order in orders:
        lines.append(str(order.user)) 
        lines.append(str(order.payment)) 
        lines.append(str(order.order)) 
        lines.append(str(order.product)) 
        lines.append(str(order.product_price)) 
        lines.append('   ') 
        

    # loop 
    for line in lines:
        textobj.textLine(line)
        

    # finish
    cnvs.drawText(textobj)
    cnvs.showPage()
    cnvs.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='weekly sales report.pdf')

def report(request):
    return render(request, 'admin_report.html')

@login_required(login_url='admin_login')
def sales_report(request):    
    if request.method == "POST":        
        from_date = request.POST["from_date"]
        to_date = request.POST["to_date"]
        orders = Order.objects.filter(created_at__range=(from_date, to_date))
        context = {
        'orders':orders,          
        }
        return render(request,'sales_report.html',context)
    
    else:
        orders = Order.objects.all().order_by('-order_number')
        context = {
            'orders':orders,            
        }
        return render(request,'sales_report.html',context)

def sales_report2(request):
    salesreports = Order.objects.all().order_by('-created_at')
    total = 0
    total= salesreports.aggregate(Sum('order_total')).get('order_total__sum')
    RoundTotal =("{:0.2f}".format(total))
    
    paginator = Paginator(salesreports, 10) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    salesreport = paginator.get_page(page_number)

    context = {
        'salesreport': salesreport ,
        'total':    total,
        'RoundTotal': RoundTotal,

    }
    return render(request,'report2.html',context)



@login_required(login_url='admin_panel')
def monthly_report(request):
    context = None
    # frmdate = date
    if request.method == "POST": 
        from_date = request.POST["from_date"]
    
    

        fm=datetime.strptime(from_date, "%d-%m-%Y")
    
        to_date = fm + timedelta(days=30)
    # fm = [ 2022 , frmdate , 1 ]
    # todt = [2022 , frmdate , 28 ]
    # fm=datetime.strptime(fm, "%d %B, %Y")
    # todt=datetime.strptime(todt, "%d %B, %Y")
    
    # print(fm)
            
        salesreport = Order.objects.filter(created_at__gte=datetime.date(fm), created_at__lte=datetime.date(to_date))
    
        if len(salesreport) > 0 :   
            context = {
                    'salesreport' : salesreport ,  
                
                }
            print(salesreport)
            print("111")
            return render(request,'search_report_sales.html',context)
            return render(request,'admin/sales_report_search.html',context)
        else:
            messages.info(request,"No Orders")
    return render(request,'report2.html',context)


@login_required(login_url='admin_panel')
def yearly_report(request):
    context = None
    frmdate = date
    if request.method == "POST": 
        from_date = request.POST["from_date"]
    
    

        fm=datetime.strptime(from_date, "%d-%m-%Y")
    
        to_date = fm + relativedelta(months=11)
   
    # fm = [ frmdate , 1 , 1 ]
    # todt = [frmdate , 12 , 30 ]

    # print(fm)
            
        salesreport = Order.objects.filter(created_at__gte=datetime.date(fm), created_at__lte=datetime.date(to_date))
        if len(salesreport) > 0 :   
            context = {
                    'salesreport' : salesreport ,   
                }
            print(salesreport)
            print("222222222222222222222222222222222222222")
            return render(request,'search_report_sales.html',context)
        else:
            print("44444444444444444")
            messages.info(request,"No Orders")
    return render(request,'report2.html',context)


@login_required(login_url='admin_panel')
def weekly_report(request,date):
    context = None
    frmdate = date
   
    fm = [ 2022 , 1 , frmdate ]
    todt = [2022 , 12 , frmdate ]
    
    print(fm)
            
    salesreport = Order.objects.filter(created_at__range=(fm, todt)).order_by('-weekly')
    if len(salesreport) > 0 :   
        context = {
                'salesreport' : salesreport ,   
            }
        print(salesreport)
        print("222222222222222222222222222222222222222")
        return render(request,'search_report_sales.html',context)
    else:
        print("44444444444444444")
        messages.info(request,"No Orders")
    return render(request,'report2.html',context)

@login_required(login_url='admin_login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_prod_variation(request):
    form = VariationForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request,'Product variation updated.')
            return redirect('add_prod_variation')
        else:
            context = {
            'form'     : form,
            }
        return render(request, 'add_prod_variation.html',context)
    else:  
        context = {
            'form'     : form,
            }
        return render(request, 'add_prod_variation.html',context)

	
