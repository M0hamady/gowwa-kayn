from django.contrib import admin
from core.models import (
    UserProfile, FirstSectionConfig, Store, StoreDepartment, MenuItem, MenuAddon, Order,
    PrintService, LibraryBook, RealEstateListing, FinishingRequest, GeoLocation, BusRoute,
    TrainSchedule, DeliveryCourier, AskJowwaQuery, PublicService, SubscriptionPlan, Wallet,
    SMSCampaign, GoogleSMTPConfig, HostingerSMTPConfig, NotificationLog, MobileDeviceAnalytics, UserVault
)

admin.site.register(UserProfile)
admin.site.register(FirstSectionConfig)
admin.site.register(Store)
admin.site.register(StoreDepartment)
admin.site.register(MenuItem)
admin.site.register(MenuAddon)
admin.site.register(Order)
admin.site.register(PrintService)
admin.site.register(LibraryBook)
admin.site.register(RealEstateListing)
admin.site.register(FinishingRequest)
admin.site.register(GeoLocation)
admin.site.register(BusRoute)
admin.site.register(TrainSchedule)
admin.site.register(DeliveryCourier)
admin.site.register(AskJowwaQuery)
admin.site.register(PublicService)
admin.site.register(SubscriptionPlan)
admin.site.register(Wallet)
admin.site.register(SMSCampaign)
admin.site.register(GoogleSMTPConfig)
admin.site.register(HostingerSMTPConfig)
admin.site.register(NotificationLog)
admin.site.register(MobileDeviceAnalytics)
admin.site.register(UserVault)
