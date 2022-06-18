from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, render
from accounts.forms import UserAddressForm
from accounts.models import UserAddresses
from adminpanel.models import ProductOffer
from cart.models import Cart, CartItem

from products.models import Products, Variation

# Create your views here.

def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart= request.session.create()
    return cart

def offer_check_function(item):
    product = Products.objects.get(product_name=item)
    print(product)
    if ProductOffer.objects.filter(product=product).exists():
     
            sub_total =  product.price -  ((product.price*product.product_offer.discount)/100) 
    
    else:
        sub_total=product.price
        print(sub_total)
    return sub_total

def add_cart(request,product_id):
    product=Products.objects.get(id=product_id) # get the product
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart=Cart.objects.create(
            cart_id=_cart_id(request)
        )
        cart.save()
    if request.user.is_authenticated:
        try:
            cart_item=CartItem.objects.get(product=product,cart=cart)
            cart_item.quantity += 1
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item=CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart,
            user=request.user
        )
        cart_item.save()
    else:
        try:
            cart_item=CartItem.objects.get(product=product,cart=cart)
            cart_item.quantity += 1
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item=CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart,
            
        )
        cart_item.save()
    return redirect('cart')

#     product=Products.objects.get(id=product_id) # get the product
#     product_variation=[]
# #    if request.user.is_authenticated:
#     if request.method=='POST':
#         for items in request.POST:
#             print('this is the request', request.POST)
#             key=items
#             value=request.POST[key]
#             print(key,value)
#             try:
#                 variation=Variation.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)
#                 product_variation.append(variation)
#             except:
#                 pass

    
#     try:
#         cart=Cart.objects.get(cart_id=_cart_id(request))
#     except Cart.DoesNotExist:
#         cart=Cart.objects.create(
#             cart_id=_cart_id(request)
#         )
#         cart.save()

#     try:
#         cart_item=CartItem.objects.get(product=product,cart=cart)
#         if len(product_variation)>0:
#               for item in product_variation:
#                 cart_item.variations.add(item)
#         cart_item.quantity += 1
#         cart_item.save()
#     except CartItem.DoesNotExist:
#         cart_item=CartItem.objects.create(
#             product=product,
#             quantity=1,
#             cart=cart,
#             user=request.user
            
#         )
#         if len(product_variation)>0:
#               for item in product_variation:
#                 cart_item.variations.add(item)
#         cart_item.quantity += 1
#         cart_item.save()
 
        # is_cart_item_exists =CartItem.objects.filter(product=product,cart=cart).exists()
        # if is_cart_item_exists:
        #     cart_item=CartItem.objects.filter(product=product,cart=cart)
        #     #existing variation
        #     #current variation and itemid
        #     ex_variations_list=[]
        #     id=[]
        #     for item in cart_item:
        #         existing_variations=item.variations.all()
        #         ex_variations_list.append(list(existing_variations))
        #         id.append(item.id)

        #     if product_variation in ex_variations_list:
        #         index=ex_variations_list.index(product_variation)
        #         item_id=id[index]
        #         item=CartItem.objects.get(product=product,id=item_id)
        #         item.quantity+=1
        #         item.save()
        #     else:
        #         item=CartItem.objects.create(product=product,
        #             quantity=1,
        #             cart=cart)
        #         if len(product_variation)>0:
        #             item.variations.clear()
        #             item.variations.add(*product_variation)   
                        
        #         item.save()
        # else:
        #     cart_item=CartItem.objects.create(
        #     product=product,
        #     quantity=1,
        #     cart=cart,
        #     user=request.user
        # )
        #     if len(product_variation)>0:
        #         cart_item.variations.clear()
        #         cart_item.variations.add(*product_variation)   
                    
        #     cart_item.save()
    # else:
    #     try:
    #         cart_item=CartItem.objects.get(product=product,cart=cart)
    #         cart_item.quantity += 1
    #         cart_item.save()
    #     except CartItem.DoesNotExist:
    #         cart_item=CartItem.objects.create(
    #         product=product,
    #         quantity=1,
    #         cart=cart,
            
    #     )
    #     cart_item.save()
    # return redirect('cart')

def remove_cart(request,product_id):
    product = get_object_or_404(Products, id=product_id)
    cart=Cart.objects.get(cart_id=_cart_id(request))
    cart_item=CartItem.objects.get(product=product,cart=cart)   
    if cart_item.quantity>1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

def remove_items(request,product_id):
    product = get_object_or_404(Products, id=product_id)
    cart=Cart.objects.get(cart_id=_cart_id(request))
    cart_item=CartItem.objects.get(product=product,cart=cart) 
    cart_item.delete()
    return redirect('cart')
    
def cart(request,total=0, quantity=0, cart_items=0):
    try:
        grand_total=0
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_items=CartItem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            new_price = offer_check_function(cart_item)
            total +=(new_price * cart_item.quantity)
            quantity += cart_item.quantity
        grand_total=total+100
    except ObjectDoesNotExist:
        pass
    context={
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'grand_total': grand_total,
        
    }

    return render(request,'cart.html',context)

@login_required(login_url='signin')
def checkout(request,total=0, quantity=0, cart_items=0):
    
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_items=CartItem.objects.filter(cart=cart,is_active=True)
        add=UserAddresses.objects.filter(user=request.user)
        form = UserAddressForm(instance=request.user)
        for cart_item in cart_items:
            new_price = offer_check_function(cart_item)
            total +=(new_price * cart_item.quantity)
            quantity += cart_item.quantity
        grand_total=total+100
        

    except:
        pass
    context={
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'grand_total': grand_total,
        'add':add,
        'form':form,
        'profile':request.user
    }
    return render(request,'checkout.html',context)