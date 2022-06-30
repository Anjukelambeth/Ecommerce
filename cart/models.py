from itertools import product
from django.db import models
from accounts.models import Account
from adminpanel.models import CategoryOffer, ProductOffer
from products.models import Products, Variation
# Create your models here.
class Cart(models.Model):
    cart_id=models.CharField(max_length=250,blank=True)
    date_added=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    variations=models.ManyToManyField(Variation,blank=True)
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    is_active=models.BooleanField(default=True)

    def sub_total(self):
        if ProductOffer.objects.filter(product=self.product).exists():
            return (self.product.price -  ((self.product.price* self.product.product_offer.discount)/100)) * self.quantity
        elif CategoryOffer.objects.filter(category=self.product.category).exists():
            return (self.product.price - ((self.product.price*self.product.category.category_offer.discount)/100)) * self.quantity
        else:
            return self.product.price * self.quantity

    def __str__(self):
        return self.product.product_name