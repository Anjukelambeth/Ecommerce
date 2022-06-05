from multiprocessing import context
from django.http import HttpResponse
from django.shortcuts import redirect, render
from datetime import datetime
from cart.models import CartItem
from orders.forms import OrderForm
from orders.models import Order, OrderProduct, Payment
import datetime

from products.models import Products
# Create your views here.
def place_order(request,total = 0,quantity = 0):
    current_user = request.user

    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    # if (cart_count <= 0):
    #     return redirect('store')
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity

    
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
            context={
                'order':order,
                'cart_items':cart_items,
                'total':total,
                
            }
            return render(request,'payments.html',context)
        else:
            return HttpResponse('form not valid')
        
    # else:
    #     return redirect('checkout')    

    return render(request,'checkout.html')

def payments(request):
    return render(request,'payments.html')

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
