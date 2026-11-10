from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from decimal import Decimal
from core.encryption import encrypt_password
from core.models import GoogleSMTPConfig, HostingerSMTPConfig, SMSCampaign, Wallet

@receiver(pre_save, sender=GoogleSMTPConfig)
def encrypt_google_smtp_password(sender, instance, **kwargs):
    if instance.encrypted_password and not instance.encrypted_password.startswith("pbkdf2_enc$"):
        instance.encrypted_password = encrypt_password(instance.encrypted_password)

@receiver(pre_save, sender=HostingerSMTPConfig)
def encrypt_hostinger_smtp_password(sender, instance, **kwargs):
    if instance.encrypted_password and not instance.encrypted_password.startswith("pbkdf2_enc$"):
        instance.encrypted_password = encrypt_password(instance.encrypted_password)

@receiver(pre_save, sender=SMSCampaign)
def enforce_sms_price_and_calculate_total(sender, instance, **kwargs):
    instance.price_per_sms = Decimal('0.75')
    instance.total_cost = Decimal(str(instance.recipient_count)) * instance.price_per_sms

@receiver(post_save, sender=SMSCampaign)
def deduct_wallet_for_sms_campaign(sender, instance, created, **kwargs):
    if created and not instance.is_processed:
        wallet = Wallet.objects.first()
        if wallet:
            wallet.balance = wallet.balance - instance.total_cost
            wallet.save()
        SMSCampaign.objects.filter(pk=instance.pk).update(is_processed=True)
