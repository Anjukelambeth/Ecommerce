from datetime import datetime, timezone
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from accounts.models import Account
from cart.models import CartItem
from refferalcode.forms import CouponApplyForm, RefferalApplyForm
from coupons.models import Coupon
from orders.models import Order
from refferalcode.models import Refferal

# Create your views here.
@require_POST
def refferalcode_apply(request):
    now = timezone.now()
    # print(now)
    form = RefferalApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            refferal = Refferal.objects.get(code__iexact = code, valid_from__lte=now, valid_to__gte=now, active = True)
            request.session['refferal_id'] = refferal.id
        except Refferal.DoesNotExist:
            request.session['refferal_id'] = None
    return redirect('signin')

@csrf_exempt
def verify_refferalcode(request):
    # print('coupon verify request received')
    now = datetime.now()
    if request.method == "POST":
        code = request.POST['code']
        # print(code,'this is the offer code')
        try:
            # print('checking coupon')
            refferal = Refferal.objects.get(code__iexact = code, valid_from__lte=now, valid_to__gte=now, active = True)
            if refferal:
                # print('coupon valid')

                try:
                    coupon_already_used = Account.objects.get(user=request.user,coupon=refferal,coupon_use_status=True)
                    # print(coupon_already_used,"coupon not available")
                    if coupon_already_used:
                        # print("coupon used")
                        # print("coupon already used")
                        context = {
                        "success":"Refferalcode already used",
                        }
                        return JsonResponse (context)
                    else:
                        # print('program runs this',coupon)
                        discount = refferal.discount
                        # print(discount)
                        order = Order.objects.get(user = request.user, is_ordered = False)
                        order_no = order.order_number
                        order.coupon = refferal
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
                        
                except:
                    discount = refferal.discount
                    # print(discount)
                    order = Order.objects.get(user = request.user, is_ordered = False)
                    order_no = order.order_number
                    order.coupon = refferal
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

