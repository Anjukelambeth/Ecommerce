import json
from django.contrib import messages
from multiprocessing import context
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from datetime import datetime
from accounts.forms import UserAddressForm
from accounts.models import Account, UserAddresses
from cart.models import CartItem
from cart.views import offer_check_function
from coupons.forms import CouponApplyForm
from orders.forms import OrderForm
from orders.models import Order, OrderProduct, Payment, RazorPay
import datetime
from datetime import date
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from products.models import Products

# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

# Create your views here.


def place_order(request, total=0, quantity=0):
    try:
        address_id = request.POST['ship_address']
        
    except:
        messages.error(request,"Please select billing address")
        return redirect('checkout')
    # print('Order place request received')
    current_user = request.user
    #if the cart count is <=0, redirect to store
    try:
        order = Order.objects.get(user=current_user, is_ordered=False)
        # order_count = order.count()
        # print('order received')

        cart_items = CartItem.objects.filter(user = current_user)
        grand_total = 0
        tax = 0
        for cart_item in cart_items:
            total   += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = round((5 * total)/100,2)
        grand_total = round(total + tax,2)

        # print('found one order and rendering')


        context             = {
            'order' : order,
            'cart_items' : cart_items,
            'total' : total,
            'tax' : tax,
            'grand_total' : grand_total,
            # 'form':form
        }
        return render(request,'payments.html',context)


    except:
        cart_items = CartItem.objects.filter(user = current_user)
        cart_count = cart_items.count()
        if cart_count <= 0:
            return redirect('store')
        

        grand_total = 0
        tax = 0
        for cart_item in cart_items:
            total   += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = round((5 * total)/100,2)
        grand_total = round(total + tax,2)
        # print('going to check the post request')
        if request.method == "POST":
            # form = OrderForm(request.POST)
            # # print(form)
            # print('POST request - going to validate')
            # if form.is_valid():
            # print('form validated, getting to the fields')
            #store all the billing information inside the table
            form = CouponApplyForm()
            address_id = request.POST['ship_address']
            # print(address_id)
            address =UserAddresses.objects.filter(id = address_id, user = request.user.id)
            for i in address:
                first_name = i.first_name
                last_name = i.last_name
                mobile = i.mobile
                email = i.email
                address_line_1 = i.address_line_1
                address_line_2 = i.address_line_2
                country = i.country
                state = i.state
                city = i.city
                zipcode=i.zipcode
            # print('collected details going to assign')
            data = Order()
            data.user           = current_user
            data.first_name     = first_name
            data.last_name      = last_name
            data.phone_number         = mobile
            data.email          = email
            data.address_line1 = address_line_1
            data.address_line2 = address_line_2
            data.country        = country
            data.state          = state
            data.city           = city
            data.zip            =   zipcode
            data.order_note     = request.POST['order_note']
            data.order_total    = grand_total
            # data.tax            = tax
            data.ip             = request.META.get('REMOTE_ADDR')
            # print('Assigned all the values and going to save')
            data.save()

            #generate order no
            yr                  = int(date.today().strftime('%Y'))
            dt                  = int(date.today().strftime('%d'))
            mt                  = int(date.today().strftime('%m'))
            d                   = date(yr,mt,dt)
            current_date        = d.strftime("%Y%m%d")

            order_number        = current_date + str(data.id)
            # print('order number generated')
            data.order_number   = order_number
            data.save()
            # print('details verified and directed to checkout')
            
            order               = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            # print('order value selected and passed to context')
             # authorize razorpay client with API Keys.
           
            #createe cliten
            razorpay_client = razorpay.Client(
            auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

            currency = 'INR'
            amount = grand_total

            #create order
            razorpay_order = razorpay_client.order.create(  {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"})
            # order id of newly created order.
        
            razorpay_order_id = razorpay_order['id']
            callback_url = 'http://127.0.0.1:8000/orders/razor_success/'   
        
            # we need to pass these details to frontend.
            context = {
            'razorpay_order_id' : razorpay_order_id,
            'razorpay_merchant_key' : settings.RAZOR_KEY_ID,
            'razorpay_amount' : amount,
            'currency' : currency ,
            'callback_url' : callback_url,
            
            'order_data':order,
            'sub_total':data.order_total,
            'cart_item':cart_item,
            'order':order,
            'cart_items':cart_items,
            'total':total,
            'grand_total':grand_total,

            }
            razor_model =RazorPay()
            razor_model.order = order
            razor_model.razor_pay = razorpay_order_id
            razor_model.save()

            
            return render(request,'payments.html',context)
        else:
            # print('entered else case/GET case and redirecting to checkout')
            return redirect('checkout')

def payments(request):
    # body=json.loads(request.body)
    # print(body)
    # return render(request,'payments.html')
    body = json.loads(request.body)
    print('BODY:',body)
    current_user = request.user
    #transaction details store
    payment = Payment()
    payment.user= current_user
    payment.payment_id = body['transID']
    payment.payment_method = body['payment_method']
    payment.amount_paid = body['total']
    payment.status = body['status']
    payment.save()

    

    #create payment details and order product table
    
    cart_item = CartItem.objects.filter(user=current_user)
    order_id = str(body['orderID'])
    print(order_id)
    #taking order_id to show the invoice
    request.session['order_id']=order_id
    order_data = Order.objects.get(order_number = order_id)

    order_data.payment=payment
    order_data.save()
    
    for item in cart_item:
        
        OrderProduct.objects.create(
        order = order_data,
        product = item.product,
        user = current_user,
        quantity = item.quantity,
        product_price = item.product.price,
        payment = payment,
        ordered = True,
        )


        #decrease the product quantity from product
        orderproduct = Products.objects.filter(id=item.product_id).first()
        orderproduct.stock = orderproduct.stock-item.quantity
        orderproduct.save()
        #delete cart item from usercart after ordered
        CartItem.objects.filter(user=current_user).delete()
  
    return JsonResponse({'completed':'success'})

def cash_on_delivery(request,order_number):
    # if request.user.is_authenticated :
    #     return redirect('cash_on_delivery')
    current_user = request.user
    order= Order.objects.get(order_number=order_number)
    

    #transaction details store
    payment = Payment()
    payment.user= current_user
    payment.payment_id = ''
    payment.payment_method = 'Cash on delivery'
    payment.amount_paid = ''
    payment.status = 'Pending'
    payment.save()
    
    order.payment=payment
    order.save()
    cart_item = CartItem.objects.filter(user=current_user)
    
    
    #taking order_id to show the invoice

    
   
    for item in cart_item:
       
        OrderProduct.objects.create(
        order = order,
        product = item.product,
        user = current_user,
        quantity = item.quantity,
        product_price = item.product.price,
        payment = payment,
        ordered = True,
        )


        #decrease the product quantity from product
        orderproduct = Products.objects.filter(id=item.product_id).first()
        orderproduct.stock = orderproduct.stock-item.quantity
        orderproduct.save()
        #delete cart item from usercart after ordered
        CartItem.objects.filter(user=current_user).delete()

    order = Order.objects.get(order_number = order_number )
    order_product = OrderProduct.objects.filter(order=order)
    transID = OrderProduct.objects.filter(order=order).first()
    context = {
        'order':order,
        'order_product':order_product,
        'transID':transID
    }
    return render(request,'success.html',context)

def paypal_complete(request):
    if request.session.get('order_id'):
        order_id = request.session.get('order_id')
        del request.session['order_id']
    else:
        return redirect('home')
    order = Order.objects.get(order_number = order_id )
    order_product = OrderProduct.objects.filter(order=order)
    transID = OrderProduct.objects.filter(order=order).first()
    context = {
        'order':order,
        'order_product':order_product,
        'transID':transID
    }
    return render(request,'success.html',context)

@csrf_exempt
def razor_success(request):
    print('razor suuuuujjjjjjjjjjj')
    transID = request.POST.get('razorpay_payment_id')
    razorpay_order_id = request.POST.get('razorpay_order_id')
    signature = request.POST.get('razorpay_signature')
    current_user = request.user
            #transaction details store
    razor = RazorPay.objects.get(razor_pay=razorpay_order_id)
    order = Order.objects.get(order_number = razor)
    print('razor success page')
    payment = Payment()
    payment.user= order.user
    payment.payment_id = transID
    payment.payment_method = "Razorpapy"
    payment.amount_paid = order.order_total
    payment.status = "Completed"
    payment.save()

    order.payment=payment

    order.save()
            
    cart_item = CartItem.objects.filter(user=order.user)
    
    
    #taking order_id to show the invoice

    
   
    for item in cart_item:
       
        OrderProduct.objects.create(
            order = order,
            product = item.product,
            user = order.user,
            quantity = item.quantity,
            product_price = item.product.price,
            payment = payment,
            ordered = True,
        )
    
        #decrease the product quantity from product
        orderproduct = Products.objects.filter(id=item.product_id).first()
        orderproduct.stock = orderproduct.stock-item.quantity
        orderproduct.save()
        #delete cart item from usercart after ordered
        CartItem.objects.filter(user=order.user).delete()
               

    order = Order.objects.get(order_number = razor )
    order_product = OrderProduct.objects.filter(order=order)
    transID = OrderProduct.objects.filter(order=order).first()
    context = {
        'order':order,
        'order_product':order_product,
        'transID':transID
    }
    return render(request,'success.html',context)


def buy_place_order(request,category_slug,product_slug, total=0):
    # try:
    #     address_id = request.POST['ship_address']
        
    # except:
    #     messages.error(request,"Please select billing address")
    #     # return redirect('buyNow')
    # # print('Order place request received')
    current_user = request.user
    # #if the cart count is <=0, redirect to store
    # try:
    #     # order = Order.objects.get(user=current_user, is_ordered=False)
    #     # order_count = order.count()
    #     # print('order received')
    #     item  = Products.objects.get(category__slug=category_slug,slug=product_slug)
    #     # cart_items = CartItem.objects.filter(user = current_user)
    #     grand_total = 0
    #     tax = 0
    #     # for cart_item in cart_items:
    #     total   += (item.price * 1)
    #     # quantity += item.quantity
    #     tax = round((5 * total)/100,2)
    #     grand_total = round(total + tax,2)

    #     # print('found one order and rendering')


    #     context             = {
    #         # 'order' : order,
    #         # 'cart_items' : cart_items,
    #         'total' : total,
    #         'item': item,
    #         'tax' : tax,
    #         'grand_total' : grand_total,
    #         # 'form':form
    #     }
    #     return render(request,'buy_payments.html',context)


    # except:
    items  = Products.objects.get(category__slug=category_slug,slug=product_slug)
    # cart_items = CartItem.objects.filter(user = current_user)
    grand_total = 0
    tax = 0
    items.quantity=1
    # for cart_item in cart_items:
    total   += (items.price * 1)
    # quantity += item.quantity
    tax = round((5 * total)/100,2)
    grand_total = round(total + tax,2)
    # print('going to check the post request')
    if request.method == "POST":
        # form = OrderForm(request.POST)
        # # print(form)
        # print('POST request - going to validate')
        # if form.is_valid():
        # print('form validated, getting to the fields')
        #store all the billing information inside the table
        form = CouponApplyForm()
        address_id = request.POST['ship_address']
        # print(address_id)
        address =UserAddresses.objects.filter(id=address_id, user = request.user.id)
        for i in address:
            first_name = i.first_name
            last_name = i.last_name
            mobile = i.mobile
            email = i.email
            address_line_1 = i.address_line_1
            address_line_2 = i.address_line_2
            country = i.country
            state = i.state
            city = i.city
            zipcode=i.zipcode
        # print('collected details going to assign')
        data = Order()
        data.user           = current_user
        data.first_name     = first_name
        data.last_name      = last_name
        data.phone_number         = mobile
        data.email          = email
        data.address_line1 = address_line_1
        data.address_line2 = address_line_2
        data.country        = country
        data.state          = state
        data.city           = city
        data.zip = zipcode
        data.order_note     = request.POST['order_note']
        data.order_total    = grand_total
        # data.tax            = tax
        data.ip             = request.META.get('REMOTE_ADDR')
        # print('Assigned all the values and going to save')
        data.save()

        #generate order no
        yr                  = int(date.today().strftime('%Y'))
        dt                  = int(date.today().strftime('%d'))
        mt                  = int(date.today().strftime('%m'))
        d                   = date(yr,mt,dt)
        current_date        = d.strftime("%Y%m%d")

        order_number        = current_date + str(data.id)
        # print('order number generated')
        data.order_number   = order_number
        data.save()
        # print('details verified and directed to checkout')
        
        order               = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
        # print('order value selected and passed to context')
            # authorize razorpay client with API Keys.
        
        #createe cliten
        razorpay_client = razorpay.Client(
        auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

        currency = 'INR'
        amount = grand_total

        #create order
        razorpay_order = razorpay_client.order.create(  {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"})
        # order id of newly created order.
    
        razorpay_order_id = razorpay_order['id']
        callback_url = 'http://127.0.0.1:8000/orders/razor_success/'   
    
        # we need to pass these details to frontend.
        context = {
        'razorpay_order_id' : razorpay_order_id,
        'razorpay_merchant_key' : settings.RAZOR_KEY_ID,
        'razorpay_amount' : amount,
        'currency' : currency ,
        'callback_url' : callback_url,
        
        'order_data':order,
        'sub_total':data.order_total,
        'items':items,
        'order':order,
        'items':items,
        'total':total,
        'grand_total':grand_total,

        }
        razor_model =RazorPay()
        razor_model.order = order
        razor_model.razor_pay = razorpay_order_id
        razor_model.save()

        
        return render(request,'buy_payments.html',context)
    else:
        # print('entered else case/GET case and redirecting to checkout')
        return redirect('buyNow')

def buy_cash_on_delivery(request,category_slug,product_slug,order_number):
    # if request.user.is_authenticated :
    #     return redirect('cash_on_delivery')
    current_user = request.user
    order= Order.objects.get(order_number=order_number)
    

    #transaction details store
    payment = Payment()
    payment.user= current_user
    payment.payment_id = ''
    payment.payment_method = 'Cash on delivery'
    payment.amount_paid = ''
    payment.status = 'Pending'
    payment.save()
    
    order.payment=payment
    order.save()
    items  = Products.objects.get(category__slug=category_slug,slug=product_slug)
    
    
    #taking order_id to show the invoice

    
   
    for item in items:
       
        OrderProduct.objects.create(
        order = order,
        product = item.product,
        user = current_user,
        quantity = item.quantity,
        product_price = item.product.price,
        payment = payment,
        ordered = True,
        )


        #decrease the product quantity from product
        orderproduct = Products.objects.filter(id=item.product_id).first()
        orderproduct.stock = orderproduct.stock-item.quantity
        orderproduct.save()
        #delete cart item from usercart after ordered
        CartItem.objects.filter(user=current_user).delete()

    order = Order.objects.get(order_number = order_number )
    order_product = OrderProduct.objects.filter(order=order)
    transID = OrderProduct.objects.filter(order=order).first()
    context = {
        'order':order,
        'order_product':order_product,
        'transID':transID,
        'item':item,
    }
    return render(request,'buy_success.html',context)