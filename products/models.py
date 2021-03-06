
from email.policy import default
from itertools import product
from django.urls import reverse
from django.db import models
from category.models import category
# Create your models here.
class Products(models.Model):
    product_name=models.CharField(max_length=200,unique=True)
    slug=models.SlugField(max_length=200,unique=True)
    product_description=models.TextField(max_length=500,blank=True)
    price= models.IntegerField()
    images  =  models.ImageField(upload_to='photos/products')
    images1 = models.ImageField(upload_to = 'photos/products', null=True, blank=True)
    images2 = models.ImageField(upload_to = 'photos/products', null=True, blank=True)
    images3 = models.ImageField(upload_to = 'photos/products',null=True, blank=True)
    images4 = models.ImageField(upload_to = 'photos/products', null=True, blank=True)
    stock=models.IntegerField()
    is_available=models.BooleanField(default=True)
    category=models.ForeignKey(category, on_delete=models.CASCADE)
    created_date=models.DateTimeField(auto_now_add=True)
    modified_date=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.product_name

class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager,self).filter(variation_category='color',is_active=True)

    def sizes(self):
        return super(VariationManager,self).filter(variation_category='size',is_active=True)

variation_category_choice=(
    ('color','color'),
    ('size','size'),
)

class Variation(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    variation_category=models.CharField(max_length=100,choices=variation_category_choice)
    variation_value=models.CharField(max_length=100)
    is_active=models.BooleanField(default=True)
    created_date=models.DateTimeField(auto_now=True)
    stock_count=models.IntegerField(null=True, blank=True)

    objects=VariationManager()
    def __str__(self) :
        return self.variation_value