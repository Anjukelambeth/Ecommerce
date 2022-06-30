from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from .utils import generate_ref_code
from accounts.models import Account
# Create your models here.
class Refferal(models.Model):
    code        = models.CharField(max_length=50,unique=True,)
    valid_from  = models.DateTimeField()
    valid_to    = models.DateTimeField()
    discount    = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(75)])
    active      = models.BooleanField()

    

    def __str__(self):
        return self.code

class ReferralCode(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    code = models.CharField(max_length=12, blank=True)
    recommended_by = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True, related_name= 'ref_by') 
    updated_at = models.DateTimeField(auto_now= True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name}-{self.code}"

    def get_recommended_profiles(self):
        refs = ReferralCode.objects.all()
        my_recommends = []
        for profile in refs:
            if profile.recommended_by == self.user:
                my_recommends.append(profile)
        return my_recommends
    def get_your_refer_code(self):
        return self.code

    def save(self, *args, **kwargs):
        if self.code == "":
            code  = generate_ref_code()
            self.code = code
        super().save(*args, **kwargs)