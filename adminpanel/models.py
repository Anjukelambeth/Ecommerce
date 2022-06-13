from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from products.models import Products

# Create your models here.
class ProductOffer(models.Model):
    product = models.OneToOneField(Products,related_name='product_offer',on_delete=models.CASCADE)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)])
    active = models.BooleanField()

    def __str__(self):
        return self.product.product_name

    def discount_amount(self,sub_total):
        return self.discount/100*sub_total