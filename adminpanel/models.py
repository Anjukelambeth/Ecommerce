from tkinter import S
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from category.models import category
from products.models import Products
from django.db.models.deletion import SET_NULL
from django.utils.translation import activate

# Create your models here.
class ProductOffer(models.Model):
    product = models.OneToOneField(Products,related_name='product_offer',on_delete=SET_NULL,null=True, blank=True)
    category=models.OneToOneField(category,on_delete=SET_NULL,null=True,blank=True)
    code    = models.CharField(max_length=50, unique=True,blank=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(75)])
    is_active = models.BooleanField()

    def __str__(self):
        return self.product.product_name

    def discount_amount(self,sub_total):
        return self.discount/100*sub_total
        
    def pro_disc_price(self):
        original_price = self.product.price
        pro_disc_price = original_price - (original_price*(self.discount/100))
        return pro_disc_price
        
class CategoryOffer(models.Model):
    category   = models.OneToOneField(category,on_delete=SET_NULL,related_name='category_offer',null=True, blank=True)
    code    = models.CharField(max_length=50, unique=True,blank=True)
    valid_from      = models.DateTimeField()
    valid_to        = models.DateTimeField()
    discount        = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(75)])
    is_active       = models.BooleanField()

    def __str__(self):
        return self.category.category_name
    
    def disc_price(self):
        original_price = self.category.product.price
        disc_price = original_price - (original_price*(self.discount/100))
        return disc_price