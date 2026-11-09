from django.contrib import admin
from .models import Store, MenuItem, Addon, DeliveryZone, SubscriptionPackage, SMSCampaign

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active', 'created_at')

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'store')

@admin.register(Addon)
class AddonAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'menu_item')

@admin.register(DeliveryZone)
class DeliveryZoneAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'fee')

@admin.register(SubscriptionPackage)
class SubscriptionPackageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price')

@admin.register(SMSCampaign)
class SMSCampaignAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'sent_at')
