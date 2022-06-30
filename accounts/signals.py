from accounts.models import Account
from refferalcode.models import  ReferralCode
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender= Account)
def post_save_create_profile(sender, instance, created, *args, **kwargs):
    if created:
        ReferralCode.objects.create(user=instance)