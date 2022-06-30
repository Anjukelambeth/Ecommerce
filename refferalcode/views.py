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
