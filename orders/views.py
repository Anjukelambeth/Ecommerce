import json
from multiprocessing import context
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from datetime import datetime
from accounts.models import Account, UserAddresses
from cart.models import CartItem
from orders.forms import OrderForm
from orders.models import Order, OrderProduct, Payment, RazorPay
import datetime
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from products.models import Products

# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

# Create your views here.
def place_order(request,total = 0,quantity = 0):
    current_user = request.user
    grand_total=0
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if (cart_count <= 0):
        return redirect('store')
    
    for cart_item in cart_items:
            total +=(cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
    grand_total=total+100

    
    if request.method=='POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            #store all billing info
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone_number = form.cleaned_data['phone_number']
            data.email = form.cleaned_data['email']
            data.address_line1 = form.cleaned_data['address_line1']
            data.address_line2 = form.cleaned_data['address_line2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.zip = form.cleaned_data['zip']
            data.order_note = form.cleaned_data['order_note']
            data.order_total=total
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            #generate order number yr/m/day/hr/mn/second
           
            order_number = str(int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
            data.order_number = order_number
            data.save()

            cart_item = CartItem.objects.filter(user=current_user)
            
           
            order = Order.objects.get(user=current_user,is_ordered=False,order_number=order_number)

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
            return HttpResponse('form not valid')

        #     context={
        #         'order':order,
        #         'cart_items':cart_items,
        #         'total':total,
        #         'grand_total':grand_total,
        #     }
        #     return render(request,'payments.html',context)
        # else:
        #     return HttpResponse('form not valid')
        
    # else:
    #     return redirect('checkout')    

    return render(request,'checkout.html')

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