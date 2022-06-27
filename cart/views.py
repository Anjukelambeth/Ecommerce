from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from accounts.forms import UserAddressForm
from accounts.models import UserAddresses
from adminpanel.models import CategoryOffer, ProductOffer
from cart.models import Cart, CartItem
from django.views.decorators.csrf import csrf_exempt
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
        if product.product_offer:
            sub_total =  product.price -  ((product.price*product.product_offer.discount)/100) 
    elif CategoryOffer.objects.filter(category=item.product.category).exists():
           if item.product.category.category_offer:
            sub_total =  product.price -  ((product.price*item.product.category.category_offer.discount)/100) 
    
    else:
        sub_total=product.price
        print(sub_total)
    return sub_total

def add_cart(request,product_id):

    current_user = request.user
    product     = Products.objects.get(id = product_id)
    # if the user is authenticated
    if current_user.is_authenticated:
        product_variation = []
        # Getting POST request:
        if request.method == 'POST':
            for item in request.POST:
                key     = item
                value   = request.POST[key]
                
                try:
                    variation   = Variation.objects.get(product = product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                    
                except:
                    pass
        # Getting a request to add a producct
        # Getting the product
        # product     = Products.objects.get(id = product_id)
        
        # Checking whether any cart is already open/ available
        # Using a private function(_cart_id), checking the availability of saved session.
        try:
            cart    = Cart.objects.get(cart_id = _cart_id(request))
        # if cart is not available, create the Cart and save.
        except Cart.DoesNotExist:
            cart    = Cart.objects.create(cart_id = _cart_id(request))
            cart.save()
        # Getting a request to add a producct
        # Getting the product
        #product     = Product.objects.get(id = product_id)
        is_cart_item_exists = CartItem.objects.filter(product = product, user=current_user).exists()
        # Adding product at the same time. Checking whether the product is already available in cart.
        # If available, increment the quantity by 1.
        if is_cart_item_exists:
            cart_item           = CartItem.objects.filter(product=product, user=current_user)
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)
            #checke
            if product_variation in ex_var_list:
                # add the new quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()

            else:
               # Getting a request to add a producct
                # create a new cart item
                item = CartItem.objects.create(product=product, cart=cart,quantity=1, user=current_user)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                    # adding a star will make surea that the star is whole thing is getting added.
                item.save() 
        # If item does not exist, create the 'cart_item'
        else:
            cart_item       = CartItem.objects.create(
                product     = product,
                quantity    = 1,
                user        = current_user,
                cart=cart
                )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        
        
        return redirect('cart')


    # if the user is not authenticated
    else:
        product_variation = []
        # Getting POST request:
        if request.method == 'POST':
            for item in request.POST:
                key     = item
                value   = request.POST[key]
                
                try:
                    variation   = Variation.objects.get(product = product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                    
                except:
                    pass
        # Getting a request to add a producct
        # Getting the product
        product     = Products.objects.get(id = product_id)
        
        # Checking whether any cart is already open/ available
        # Using a private function(_cart_id), checking the availability of saved session.
        try:
            cart    = Cart.objects.get(cart_id = _cart_id(request))
        # if cart is not available, create the Cart and save.
        except Cart.DoesNotExist:
            cart    = Cart.objects.create(cart_id = _cart_id(request))
            cart.save()

        is_cart_item_exists = CartItem.objects.filter(product = product, cart = cart).exists()
        # Adding product at the same time. Checking whether the product is already available in cart.
        # If available, increment the quantity by 1.
        if is_cart_item_exists:
            cart_item           = CartItem.objects.filter(product=product, cart=cart)
            # we need 
            # existing variations - in database 
            # current variations - new entry
            # item_id
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                # the result of the below will be a queryset. this is converted to list.
                ex_var_list.append(list(existing_variation))
                id.append(item.id)
            
            if product_variation in ex_var_list:
                # add the new quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()

            else:
                # create a new cart item
                item = CartItem.objects.create(product=product, quantity=1, cart=cart)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                    # adding a star will make surea that the star is whole thing is getting added.
                item.save() 
        # If item does not exist, create the 'cart_item'
        else:
            
            cart_item       = CartItem.objects.create(
                product     = product,
                quantity    = 1,
                cart        = cart,
                )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        
        return redirect('cart')



def remove_cart(request,product_id,cart_item_id):
    product = get_object_or_404(Products, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item   = CartItem.objects.get(product = product, user=request.user, id=cart_item_id)
        else:
            cart        = Cart.objects.get(cart_id=_cart_id(request))
            cart_item   = CartItem.objects.get(product = product, cart = cart, id=cart_item_id)
        
        if cart_item.quantity >1:
            cart_item.quantity -=1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass    
    # product = get_object_or_404(Products, id=product_id)
    # cart=Cart.objects.get(cart_id=_cart_id(request))
    # cart_item=CartItem.objects.get(product=product,cart=cart)   
    # if cart_item.quantity>1:
    #     cart_item.quantity -= 1
    #     cart_item.save()
    # else:
    #     cart_item.delete()
    return redirect('cart')

def remove_items(request):
    product_id =request.GET['prod_id']
    cart_item_id = request.GET['cartitem']

    
    # cart_item_id = request.GET['cartitem']
   
    
    product     = get_object_or_404(Products, id=product_id)
    if request.user.is_authenticated:
        cart_item   = CartItem.objects.get(product = product, user = request.user, id=cart_item_id)
    else:
        cart        = Cart.objects.get(cart_id=_cart_id(request))
        cart_item   = CartItem.objects.get(product = product, cart = cart, id=cart_item_id)
    cart_item.delete()
    return JsonResponse({'success':'Item successfully Removed'})

    # product = get_object_or_404(Products, id=product_id)
    # cart=Cart.objects.get(cart_id=_cart_id(request))
    # cart_item=CartItem.objects.get(product=product,cart=cart) 
    # cart_item.delete()
    # return redirect('cart')
    
def cart(request,total=0, quantity=0, cart_items=None):
    try:
        grand_total=0
       
        
        if request.user.is_authenticated:
            cart_items=CartItem.objects.filter(user=request.user,is_active=True).order_by('id')
        else:
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_items=CartItem.objects.filter(cart=cart,is_active=True).order_by('id')
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
        
        if request.user.is_authenticated:
            cart_items  = CartItem.objects.filter(user=request.user, is_active = True)
        # cart=Cart.objects.get(cart_id=_cart_id(request))
        # cart_items=CartItem.objects.filter(cart=cart,is_active=True)
            address=UserAddresses.objects.filter(user=request.user.id).order_by('-id')[:3]
            # form = UserAddressForm(instance=request.user)
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
        'address':address,
        # 'form':form,
        'profile':request.user
    }
    return render(request,'checkout.html',context)

@csrf_exempt
def add_cart_ajax(request):
    product_id = request.POST['id']
    current_user = request.user
    product     = Products.objects.get(id = product_id)
    
    # if the user is authenticated
    if current_user.is_authenticated:
        product_variation = []
        # Getting POST request:
        if request.method == 'POST':
            
            
            for item in request.POST:
                key     = item
                value   = request.POST[key]
                
                try:
                    variation   = Variation.objects.get(product = product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                    
                except:
                    pass
        # Getting a request to add a producct
        # Getting the product
        #product     = Product.objects.get(id = product_id)


        is_cart_item_exists = CartItem.objects.filter(product = product, user=current_user).exists()
        # Adding product at the same time. Checking whether the product is already available in cart.
        # If available, increment the quantity by 1.
        if is_cart_item_exists:
            cart_item           = CartItem.objects.filter(product=product, user=current_user)
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)
            #checke
            if product_variation in ex_var_list:
                
                # add the new quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()

        
            success = 'Product added to cart..!'
            cart_count = CartItem.objects.filter(user=current_user).count()
            
            return JsonResponse({'success': success,'cart_count':cart_count})

 # Adding function to remove cart

def remove_cart_ajax(request):
    product_id =request.GET['prod_id']
    cart_item_id = request.GET['cart_id']
    
    product     = get_object_or_404(Products, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item   = CartItem.objects.get(product = product, user=request.user, id=cart_item_id)
        else:
            cart        = Cart.objects.get(cart_id=_cart_id(request))
            cart_item   = CartItem.objects.get(product = product, cart = cart, id=cart_item_id)
        
        if cart_item.quantity >1:
            cart_item.quantity -=1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass    
    return JsonResponse({'success':'Item successfully Removed'})

@login_required(login_url='signin')
def buyNow(request,category_slug,product_slug,total=0, quantity=0,):
    grand_total=0
    try:
        if request.user.is_authenticated:
            item  = Products.objects.get(category__slug=category_slug,slug=product_slug)
        # cart=Cart.objects.get(cart_id=_cart_id(request))
        # cart_items=CartItem.objects.filter(cart=cart,is_active=True)
            address=UserAddresses.objects.filter(user=request.user)
            # form = UserAddressForm(instance=request.user)
            item.quantity=1
            new_price = offer_check_function(item)
            total += new_price * 1
            
        grand_total=total+100
        

    except:
        pass
    context={
        'total': total,
        'quantity': quantity,
        'item': item,
        'grand_total': grand_total,
         'address':address,
        # 'form':form,
        'profile':request.user
    }
    return render(request,'buyNow.html',context)


