from datetime import datetime, timezone
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from cart.models import CartItem
from cart.views import offer_check_function
from coupons.forms import CouponApplyForm
from coupons.models import Coupon
from orders.models import Order

# Create your views here.
@require_POST
def coupon_apply(request):
    now = timezone.now()
    # print(now)
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact = code, valid_from__lte=now, valid_to__gte=now, active = True)
            request.session['coupon_id'] = coupon.id
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
    return redirect('payments')

@csrf_exempt
def verify_coupon(request):
    # print('coupon verify request received')
    now = datetime.now()
    if request.method == "POST":
        code = request.POST['code']
        # print(code,'this is the offer code')
        try:
            # print('checking coupon')
            coupon = Coupon.objects.get(code__iexact = code, valid_from__lte=now, valid_to__gte=now, active = True)
            if coupon:
                print('coupon valid')

               
                # print('program runs this',coupon)
                discount = coupon.discount
                print(discount)
              
                print(9000)
                print('got order')
                current_user = request.user
                cart_items = CartItem.objects.filter(user = current_user)
                grand_total = 0
                tax = 0
                total = 0
                quantity = 0
                for cart_item in cart_items:
                    new_price = offer_check_function(cart_item)
                    total   += (new_price * cart_item.quantity)
                    quantity += cart_item.quantity
                
                grand_total = round(total + 100)
                print(grand_total,'8888')
                discount_amount = round(grand_total * discount/100,2)
                print(discount_amount,'discount amount')
                total_after_coupon = round(float(grand_total - discount_amount),2)
                print(grand_total,'total')
                print(total_after_coupon,'amount after discount')
                print(9999)
                context = {
                    "success":"valid",
                    "discount_amount": discount_amount,
                    "total_after_coupon":total_after_coupon,
                }
                return JsonResponse(context)
                        
            else:   # except:
                discount = coupon.discount
                # print(discount)
                order = Order.objects.get(user = request.user, is_ordered = False)
                order_no = order.order_number
                order.coupon = coupon
                order.discount = round(discount,2)
                order.save()
                # print(order_no)
                # print('got order')
                current_user = request.user
                cart_items = CartItem.objects.filter(user = current_user)
                grand_total = 0
                tax = 0
                total = 0
                quantity = 0
                for cart_item in cart_items:
                    total   += (cart_item.product.price * cart_item.quantity)
                    quantity += cart_item.quantity
                tax = round((5 * total)/100,2)
                grand_total = round(total + tax,2)
            
                discount_amount = round(grand_total * discount/100,2)
                # print(discount_amount,'discount amount')
                total_after_coupon = round(float(grand_total - discount_amount),2)
                # print(grand_total,'total')
                # print(total_after_coupon,'amount after discount')

                context = {
                    "success":"valid",
                    "discount_amount": discount_amount,
                    "total_after_coupon":total_after_coupon,
                }
                return JsonResponse(context)                    
                    
        except Coupon.DoesNotExist:
            # print('no coupon available')
            context = {
                "success":"no_coupon",
            }
            return JsonResponse (context)

