from django.db import models
from decimal import Decimal

# 1. accounts_roles
class UserProfile(models.Model):
    user_name = models.CharField(max_length=150, verbose_name="اسم المستخدم / الحساب")
    phone = models.CharField(max_length=20, verbose_name="رقم الهاتف", blank=True, null=True)
    role = models.CharField(max_length=50, default='user', verbose_name="الدور الوظيفي")
    bio = models.TextField(blank=True, verbose_name="نبذة مختصرة")

    class Meta:
        app_label = 'accounts_roles'
        verbose_name = "ملف المستخدم والأدوار"
        verbose_name_plural = "إدارة الحسابات والأدوار"
        constraints = [
            models.UniqueConstraint(fields=['phone'], name='unique_user_phone_accounts')
        ]

    def __str__(self):
        return f"{self.user_name} ({self.role})"

# 2. hero_customizer
class FirstSectionConfig(models.Model):
    title = models.CharField(max_length=255, verbose_name="العنوان الرئيسي لـ Hero")
    subtitle = models.CharField(max_length=255, verbose_name="العنوان الفرعي", blank=True)
    banner_image_url = models.URLField(blank=True, verbose_name="رابط الصورة")
    is_active = models.BooleanField(default=True, verbose_name="مفعل")

    class Meta:
        app_label = 'hero_customizer'
        verbose_name = "إعداد القسم الأول (Hero)"
        verbose_name_plural = "تخصيص الهيرو والواجهة"

    def __str__(self):
        return self.title

# 3. stores_pos
class Store(models.Model):
    name = models.CharField(max_length=255, verbose_name="اسم المحل")
    provider_type = models.CharField(max_length=50, default='restaurant_bakery', verbose_name="نوع النشاط")
    address = models.CharField(max_length=255, blank=True, verbose_name="العنوان")
    phone = models.CharField(max_length=20, blank=True, verbose_name="الهاتف")
    is_active = models.BooleanField(default=True, verbose_name="نشط")

    class Meta:
        app_label = 'stores_pos'
        verbose_name = "محل / متجر"
        verbose_name_plural = "المحلات ونقاط البيع"

    def __str__(self):
        return self.name

class StoreDepartment(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='departments', verbose_name="المحل")
    name = models.CharField(max_length=255, verbose_name="اسم القسم")
    description = models.TextField(blank=True, verbose_name="الوصف")
    is_active = models.BooleanField(default=True, verbose_name="نشط")

    class Meta:
        app_label = 'stores_pos'
        verbose_name = "قسم بالمحل"
        verbose_name_plural = "أقسام المحلات"

    def __str__(self):
        return f"{self.store.name} - {self.name}"

class MenuItem(models.Model):
    department = models.ForeignKey(StoreDepartment, on_delete=models.CASCADE, related_name='items', verbose_name="القسم")
    name = models.CharField(max_length=255, verbose_name="اسم الصنف")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="السعر")
    is_available = models.BooleanField(default=True, verbose_name="متاح")

    class Meta:
        app_label = 'stores_pos'
        verbose_name = "صنف منيو"
        verbose_name_plural = "أصناف المنيو"
        constraints = [
            models.CheckConstraint(check=models.Q(price__gte=Decimal('0.00')), name='menuitem_price_gte_zero')
        ]

    def __str__(self):
        return self.name

class MenuAddon(models.Model):
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='addons', verbose_name="الصنف")
    name = models.CharField(max_length=255, verbose_name="اسم الإضافة")
    extra_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    class Meta:
        app_label = 'stores_pos'
        verbose_name = "إضافة منيو"
        verbose_name_plural = "إضافات المنيو"

    def __str__(self):
        return f"{self.name} (+{self.extra_price})"

class Order(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, verbose_name="المحل")
    customer_name = models.CharField(max_length=255, verbose_name="اسم العميل", blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    status = models.CharField(max_length=50, default='pending', verbose_name="حالة الطلب")

    class Meta:
        app_label = 'stores_pos'
        verbose_name = "طلب POS"
        verbose_name_plural = "طلبات المحلات"

    def __str__(self):
        return f"طلب #{self.id} - {self.store.name}"

# 4. printing_libraries
class PrintService(models.Model):
    title = models.CharField(max_length=255, verbose_name="خدمة الطباعة")
    paper_size = models.CharField(max_length=20, default='A4', verbose_name="مقاس الورق")
    color_mode = models.CharField(max_length=20, default='BW', verbose_name="ألوان / أسود")
    price_per_page = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('1.00'))

    class Meta:
        app_label = 'printing_libraries'
        verbose_name = "خدمة طباعة"
        verbose_name_plural = "الطباعة والمكتبات"

    def __str__(self):
        return self.title

class LibraryBook(models.Model):
    title = models.CharField(max_length=255, verbose_name="اسم الكتاب")
    author = models.CharField(max_length=255, blank=True, verbose_name="المؤلف")
    isbn = models.CharField(max_length=50, unique=True, verbose_name="الرقم المعياري ISBN")
    available_copies = models.IntegerField(default=1, verbose_name="النسخ المتاحة")

    class Meta:
        app_label = 'printing_libraries'
        verbose_name = "كتاب مكتبة"
        verbose_name_plural = "كتب المكتبات"
        constraints = [
            models.UniqueConstraint(fields=['isbn'], name='unique_book_isbn_meta')
        ]

    def __str__(self):
        return self.title

# 5. realestate_finishing
class RealEstateListing(models.Model):
    title = models.CharField(max_length=255, verbose_name="عنوان العقار")
    listing_type = models.CharField(max_length=50, default='sale', verbose_name="بيع / إيجار / تنازل")
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="السعر")
    location = models.CharField(max_length=255, blank=True, verbose_name="الموقع")

    class Meta:
        app_label = 'realestate_finishing'
        verbose_name = "عقار / تنازل"
        verbose_name_plural = "العقارات والتشطيبات"

    def __str__(self):
        return self.title

class FinishingRequest(models.Model):
    client_name = models.CharField(max_length=255, verbose_name="اسم العميل")
    property_type = models.CharField(max_length=100, verbose_name="نوع الوحدة (شقة/فيلا)")
    budget = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="الميزانية")
    description = models.TextField(blank=True, verbose_name="تفاصيل التشطيب")

    class Meta:
        app_label = 'realestate_finishing'
        verbose_name = "طلب تشطيب"
        verbose_name_plural = "طلبات التشطيب"

    def __str__(self):
        return f"تشطيب: {self.client_name}"

# 6. map_geo
class GeoLocation(models.Model):
    name = models.CharField(max_length=255, verbose_name="اسم الموقع")
    latitude = models.FloatField(verbose_name="خط العرض")
    longitude = models.FloatField(verbose_name="خط الطول")
    category = models.CharField(max_length=100, blank=True, verbose_name="التصنيف الجغرافي")

    class Meta:
        app_label = 'map_geo'
        verbose_name = "موقع جغرافي"
        verbose_name_plural = "الخرائط والمواقع الجغرافية"

    def __str__(self):
        return self.name

# 7. transit_hub
class BusRoute(models.Model):
    route_name = models.CharField(max_length=255, verbose_name="اسم خط الباص")
    origin = models.CharField(max_length=255, verbose_name="محطة القيام")
    destination = models.CharField(max_length=255, verbose_name="محطة الوصول")
    ticket_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="سعر التذكرة")

    class Meta:
        app_label = 'transit_hub'
        verbose_name = "خط باص"
        verbose_name_plural = "مواقف الباصات والقطارات والمناديب"

    def __str__(self):
        return self.route_name

class TrainSchedule(models.Model):
    train_number = models.CharField(max_length=50, verbose_name="رقم القطار / الرحلة")
    departure_time = models.CharField(max_length=50, verbose_name="موعد المغادرة")
    arrival_time = models.CharField(max_length=50, verbose_name="موعد الوصول")

    class Meta:
        app_label = 'transit_hub'
        verbose_name = "جدول قطار"
        verbose_name_plural = "جداول القطارات"

    def __str__(self):
        return f"قطار {self.train_number}"

class DeliveryCourier(models.Model):
    name = models.CharField(max_length=255, verbose_name="اسم المندوب")
    phone = models.CharField(max_length=20, verbose_name="الهاتف")
    vehicle_type = models.CharField(max_length=50, default='motorcycle', verbose_name="وسيلة التوصيل")
    is_available = models.BooleanField(default=True, verbose_name="متاح للعمل")

    class Meta:
        app_label = 'transit_hub'
        verbose_name = "مندوب توصيل"
        verbose_name_plural = "مناديب التوصيل"

    def __str__(self):
        return self.name

# 8. ai_assistant
class AskJowwaQuery(models.Model):
    user_prompt = models.TextField(verbose_name="سؤال العميل (اسأل جوه)")
    ai_response = models.TextField(blank=True, verbose_name="إجابة المساعد الذكي")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الاستفسار")

    class Meta:
        app_label = 'ai_assistant'
        verbose_name = "استفسار اسأل جوه"
        verbose_name_plural = "مساعد الذكاء الاصطناعي - اسأل جوه"

    def __str__(self):
        return f"استفسار: {self.user_prompt[:30]}"

# 9. services_directory
class PublicService(models.Model):
    title = models.CharField(max_length=255, verbose_name="عنوان الخدمة")
    category = models.CharField(max_length=100, verbose_name="تصنيف الخدمة العامة")
    phone = models.CharField(max_length=20, blank=True, verbose_name="رقم التواصل")
    description = models.TextField(blank=True, verbose_name="تفاصيل الخدمة")

    class Meta:
        app_label = 'services_directory'
        verbose_name = "خدمة عامة"
        verbose_name_plural = "دليل الخدمات العامة"

    def __str__(self):
        return self.title

# 10. subscriptions_sms
class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=255, verbose_name="اسم الباقة")
    monthly_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="الاشتراك الشهري")
    features = models.TextField(blank=True, verbose_name="المميزات")

    class Meta:
        app_label = 'subscriptions_sms'
        verbose_name = "باقة اشتراك"
        verbose_name_plural = "الاشتراكات وحملات الرسائل"

    def __str__(self):
        return self.name

class Wallet(models.Model):
    user_name = models.CharField(max_length=150, unique=True, verbose_name="اسم المستخدم")
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'), verbose_name="رصيد المحفظة")

    class Meta:
        app_label = 'subscriptions_sms'
        verbose_name = "محفظة رصيد"
        verbose_name_plural = "محافظ المستخدين"
        constraints = [
            models.CheckConstraint(check=models.Q(balance__gte=Decimal('0.00')), name='wallet_balance_gte_zero'),
            models.UniqueConstraint(fields=['user_name'], name='unique_wallet_user_meta')
        ]

    def __str__(self):
        return f"محفظة {self.user_name}: {self.balance} ج.م"

class SMSCampaign(models.Model):
    campaign_name = models.CharField(max_length=255, verbose_name="اسم الحملة")
    message_body = models.TextField(verbose_name="نص الرسالة")
    recipient_count = models.IntegerField(default=1, verbose_name="عدد المستلمين")
    price_per_sms = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.75'), verbose_name="سعر الرسالة (0.75 ج.م)")
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.75'), verbose_name="إجمالي تكلفة الحملة")
    is_processed = models.BooleanField(default=False, verbose_name="تم الخصم والمعالجة")

    class Meta:
        app_label = 'subscriptions_sms'
        verbose_name = "حملة رسائل SMS"
        verbose_name_plural = "حملات الرسائل SMS (75 قرش)"
        constraints = [
            models.CheckConstraint(check=models.Q(price_per_sms=Decimal('0.75')), name='sms_price_75_piasters')
        ]

    def __str__(self):
        return f"{self.campaign_name} ({self.recipient_count} رسائل)"

# 11. notifications_mailer
class GoogleSMTPConfig(models.Model):
    email_address = models.EmailField(unique=True, verbose_name="إيميل جوجل (Gmail)")
    encrypted_password = models.CharField(max_length=255, verbose_name="كلمة المرور المشفرة")
    smtp_host = models.CharField(max_length=255, default='smtp.gmail.com', verbose_name="سيرفر SMTP")
    smtp_port = models.IntegerField(default=587, verbose_name="البورت")

    class Meta:
        app_label = 'notifications_mailer'
        verbose_name = "إعدادات إيميل Google"
        verbose_name_plural = "الإشعارات وربط الإيميلات"
        constraints = [
            models.UniqueConstraint(fields=['email_address'], name='unique_google_email_meta')
        ]

    def __str__(self):
        return f"Google: {self.email_address}"

class HostingerSMTPConfig(models.Model):
    email_address = models.EmailField(unique=True, verbose_name="إيميل هوستنجر (Hostinger)")
    encrypted_password = models.CharField(max_length=255, verbose_name="كلمة المرور المشفرة")
    smtp_host = models.CharField(max_length=255, default='smtp.hostinger.com', verbose_name="سيرفر SMTP")
    smtp_port = models.IntegerField(default=465, verbose_name="البورت")

    class Meta:
        app_label = 'notifications_mailer'
        verbose_name = "إعدادات إيميل Hostinger"
        verbose_name_plural = "إعدادات إيميلات Hostinger"
        constraints = [
            models.UniqueConstraint(fields=['email_address'], name='unique_hostinger_email_meta')
        ]

    def __str__(self):
        return f"Hostinger: {self.email_address}"

class NotificationLog(models.Model):
    recipient = models.CharField(max_length=255, verbose_name="المستلم")
    subject = models.CharField(max_length=255, verbose_name="العنوان")
    status = models.CharField(max_length=50, default='sent', verbose_name="حالة الإرسال")

    class Meta:
        app_label = 'notifications_mailer'
        verbose_name = "سجل الإشعارات"
        verbose_name_plural = "سجلات الإشعارات"

    def __str__(self):
        return f"إشعار إلى {self.recipient}"

# 12. device_analytics
class MobileDeviceAnalytics(models.Model):
    device_uuid = models.CharField(max_length=100, unique=True, verbose_name="معرف الجهاز UUID")
    user_agent = models.CharField(max_length=255, blank=True, verbose_name="User Agent")
    ip_address = models.CharField(max_length=45, blank=True, verbose_name="عنوان IP")
    last_endpoint = models.CharField(max_length=255, blank=True, verbose_name="آخر مسار")

    class Meta:
        app_label = 'device_analytics'
        verbose_name = "تحليل جهاز موبايل"
        verbose_name_plural = "تحليلات الأجهزة والخزنة"
        constraints = [
            models.UniqueConstraint(fields=['device_uuid'], name='unique_device_uuid_meta')
        ]

    def __str__(self):
        return f"جهاز {self.device_uuid[:8]}"

class UserVault(models.Model):
    user_identifier = models.CharField(max_length=150, verbose_name="معرف المستخدم")
    encrypted_data = models.TextField(verbose_name="البيانات المشفرة بالخزنة")

    class Meta:
        app_label = 'device_analytics'
        verbose_name = "خزنة مستخدم"
        verbose_name_plural = "خزانات المستخدمين"

    def __str__(self):
        return f"خزنة {self.user_identifier}"
