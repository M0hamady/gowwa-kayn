from django.db import models

class Store(models.Model):
    PROVIDER_TYPE_CHOICES = [
        ('restaurant_bakery', 'مطاعم وحلويات وكافيهات'),
        ('supermarket_retail', 'سوبر ماركت ومحلات متعددة الأقسام'),
        ('bookstore_printing', 'مكتبات ومطابع'),
        ('real_estate_agency', 'عقارات ومكاتب تسويق عقاري'),
        ('home_service', 'خدمات منزلية وصيانة وغسيل سيارات'),
        ('delivery_fleet', 'مناديب توصيل وسائقي أفراد'),
    ]

    name = models.CharField(max_length=255, verbose_name="اسم النشاط / المحل")
    provider_type = models.CharField(
        max_length=50, 
        choices=PROVIDER_TYPE_CHOICES, 
        default='restaurant_bakery',
        verbose_name="نوع النشاط / القطاع"
    )
    address = models.CharField(max_length=255, blank=True, verbose_name="العنوان")
    phone = models.CharField(max_length=20, blank=True, verbose_name="رقم الهاتف")
    is_active = models.BooleanField(default=True, verbose_name="نشط")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")

    class Meta:
        verbose_name = "محل / مزود خدمة"
        verbose_name_plural = "المحلات ومزودو الخدمات"

    def __str__(self):
        return f"{self.name} ({self.get_provider_type_display()})"


class StoreDepartment(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='departments', verbose_name="المحل / المزود")
    name = models.CharField(max_length=255, verbose_name="اسم القسم الداخلي")
    description = models.TextField(blank=True, verbose_name="وصف القسم")
    is_active = models.BooleanField(default=True, verbose_name="نشط")

    class Meta:
        verbose_name = "قسم داخلي بالمحل"
        verbose_name_plural = "أقسام المحلات الداخلية"

    def __str__(self):
        return f"{self.name} - {self.store.name}"


class MenuItem(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='menu_items', verbose_name="المحل")
    department = models.ForeignKey(StoreDepartment, on_delete=models.SET_NULL, null=True, blank=True, related_name='items', verbose_name="القسم الداخلي")
    name = models.CharField(max_length=255, verbose_name="اسم المنتج / الخدمة")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="السعر")
    description = models.TextField(blank=True, verbose_name="الوصف")
    is_available = models.BooleanField(default=True, verbose_name="متوفر")

    class Meta:
        verbose_name = "منتج / صنف"
        verbose_name_plural = "قائمة المنتجات والأصناف"

    def __str__(self):
        return f"{self.name} ({self.price} ج.م)"


class Addon(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='addons', verbose_name="المنتج الأصلي")
    name = models.CharField(max_length=255, verbose_name="اسم الإضافة")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="سعر الإضافة")

    class Meta:
        verbose_name = "إضافة منتج"
        verbose_name_plural = "إضافات المنتجات"

    def __str__(self):
        return f"{self.name} (+{self.price} ج.م)"


class PrintingOrder(models.Model):
    ORDER_TYPE_CHOICES = [
        ('paper', 'طباعة ورقية ومذكرات (PDF)'),
        ('personalized', 'طباعة مخصصة (هدايا ومجات وتيشيرتات)'),
        ('ready', 'أدوات مكتبية ومطبوعات جاهزة'),
    ]

    PAPER_SIZE_CHOICES = [
        ('A4', 'A4'),
        ('A3', 'A3'),
    ]

    COLOR_CHOICES = [
        ('bw', 'أبيض وأسود'),
        ('color', 'ألوان'),
    ]

    BINDING_CHOICES = [
        ('none', 'بدون تكعيب'),
        ('spiral', 'تكعيب حلزوني'),
    ]

    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True, blank=True, related_name='printing_orders', verbose_name="المكتبة / المطبعة")
    order_type = models.CharField(max_length=20, choices=ORDER_TYPE_CHOICES, verbose_name="نوع طلب الطباعة")
    customer_name = models.CharField(max_length=255, verbose_name="اسم العميل")
    customer_phone = models.CharField(max_length=20, verbose_name="رقم الهاتف")
    
    total_pages = models.PositiveIntegerField(default=1, verbose_name="عدد الصفحات")
    paper_size = models.CharField(max_length=10, choices=PAPER_SIZE_CHOICES, default='A4', verbose_name="حجم الورق")
    color_mode = models.CharField(max_length=10, choices=COLOR_CHOICES, default='bw', verbose_name="نوع الألوان")
    binding_type = models.CharField(max_length=10, choices=BINDING_CHOICES, default='none', verbose_name="التكعيب")
    
    item_type = models.CharField(max_length=100, blank=True, verbose_name="نوع الخامة/الهدية (مج، تيشيرت، إلخ)")
    customization_details = models.TextField(blank=True, verbose_name="تفاصيل الطباعة المخصصة والاسم")
    
    ready_item_name = models.CharField(max_length=255, blank=True, verbose_name="اسم المنتج الجاهز / الأدوات المكتبية")
    quantity = models.PositiveIntegerField(default=1, verbose_name="الكمية")

    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="التكلفة الإجمالية")
    status = models.CharField(max_length=50, default='pending', verbose_name="حالة الطلب")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الطلب")

    class Meta:
        verbose_name = "طلب طباعة ومكتبات"
        verbose_name_plural = "طلبات المكتبات والطباعة"

    def __str__(self):
        return f"طلب طباعة #{self.id} - {self.get_order_type_display()} ({self.customer_name})"


class RealEstateListing(models.Model):
    TRANSACTION_TYPES = [
        ('rent_furnished', 'إيجار مفروش'),
        ('rent_standard', 'إيجار جديد'),
        ('sale_cash', 'بيع كاش'),
        ('sale_installments', 'بيع بالتقسيط'),
    ]

    PROPERTY_TYPES = [
        ('apartment', 'شقة سكنية'),
        ('villa', 'فيلا'),
        ('shop', 'محل تجاري'),
        ('office', 'مكتب إداري'),
    ]

    DISTRICT_CHOICES = [
        ('karma_1', 'كرمة 1'),
        ('karma_2', 'كرمة 2'),
        ('alyasmeen', 'الياسمين'),
        ('alnarges', 'النرجس'),
        ('al_salhiya_al_jadida', 'الصالحية الجديدة'),
    ]

    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True, blank=True, related_name='real_estate_listings', verbose_name="مكتب التسويق العقاري")
    title = models.CharField(max_length=255, verbose_name="عنوان الإعلان العقاري")
    transaction_type = models.CharField(max_length=30, choices=TRANSACTION_TYPES, verbose_name="نوع المعاملة")
    property_type = models.CharField(max_length=30, choices=PROPERTY_TYPES, verbose_name="نوع الوحدة")
    district = models.CharField(max_length=50, choices=DISTRICT_CHOICES, verbose_name="المنطقة / الحي")
    area_sqm = models.PositiveIntegerField(verbose_name="المساحة (متر مربع)")
    bedrooms = models.PositiveIntegerField(default=1, verbose_name="عدد الغرف")
    bathrooms = models.PositiveIntegerField(default=1, verbose_name="عدد الحمامات")
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="السعر (جنيه)")
    is_available = models.BooleanField(default=True, verbose_name="متاح للعرّض")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإضافة")

    class Meta:
        verbose_name = "وحدة عقارية"
        verbose_name_plural = "العقارات والوحدات السكنية والتجارية"

    def __str__(self):
        return f"{self.title} - {self.get_district_display()} ({self.price} ج.م)"


class PropertyInquiry(models.Model):
    listing = models.ForeignKey(RealEstateListing, on_delete=models.CASCADE, related_name='inquiries', verbose_name="الوحدة العقارية")
    client_name = models.CharField(max_length=255, verbose_name="اسم العميل")
    client_phone = models.CharField(max_length=20, verbose_name="رقم الهاتف")
    preferred_date = models.CharField(max_length=100, verbose_name="موعد المعاينة المقترح")
    notes = models.TextField(blank=True, verbose_name="ملاحظات وطلبات خاصة")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الطلب")

    class Meta:
        verbose_name = "طلب معاينة عقار"
        verbose_name_plural = "طلبات معاينة العقارات"

    def __str__(self):
        return f"معاينة {self.listing.title} بواسطة {self.client_name}"


class ServiceBooking(models.Model):
    CATEGORY_CHOICES = [
        ('maintenance', 'صيانة العامة'),
        ('plumbing', 'سباكة'),
        ('electricity', 'كهرباء'),
        ('car_wash', 'غسيل سيارات'),
        ('home_cleaning', 'نظافة منزلية'),
    ]

    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True, blank=True, related_name='service_bookings', verbose_name="مقدم الخدمة")
    service_name = models.CharField(max_length=255, verbose_name="اسم الخدمة")
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, verbose_name="تصنيف الخدمة")
    customer_name = models.CharField(max_length=255, verbose_name="اسم العميل")
    customer_phone = models.CharField(max_length=20, verbose_name="رقم الهاتف")
    address = models.CharField(max_length=255, verbose_name="العنوان وتفاصيل الموقع")
    booking_date = models.CharField(max_length=100, verbose_name="الموعد المطلوب")
    status = models.CharField(max_length=50, default='confirmed', verbose_name="حالة الحجز")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الحجز")

    class Meta:
        verbose_name = "حجز خدمة منزلية / صيانة"
        verbose_name_plural = "طلبات الخدمات المنزلية والصيانة"

    def __str__(self):
        return f"حجز {self.service_name} - {self.customer_name}"


class CourierDriver(models.Model):
    DRIVER_TYPE_CHOICES = [
        ('product_courier', 'مندوب توصيل طلبات المحلات (CourierBid)'),
        ('passenger_driver', 'سائق توصيل أفراد ومشاوير داخل كيان والصالحية'),
    ]

    name = models.CharField(max_length=255, verbose_name="اسم المندوب / السائق")
    phone = models.CharField(max_length=20, verbose_name="رقم الهاتف")
    driver_type = models.CharField(max_length=30, choices=DRIVER_TYPE_CHOICES, verbose_name="تخصص التوصيل")
    vehicle_type = models.CharField(max_length=100, verbose_name="نوع المركبة (سكوتر / دراجة / سيارة)")
    is_available = models.BooleanField(default=True, verbose_name="متاح لاستلام الطلبات")
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.00, verbose_name="التقييم")

    class Meta:
        verbose_name = "مندوب / سائق"
        verbose_name_plural = "مناديب التوصيل وسائقو الأفراد"

    def __str__(self):
        return f"{self.name} - {self.get_driver_type_display()}"


class DeliveryDispatch(models.Model):
    DISPATCH_TYPE_CHOICES = [
        ('product', 'توصيل شحنات ومنتجات'),
        ('passenger', 'مشوار نقل أفراد'),
    ]

    store = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True, blank=True, related_name='dispatches', verbose_name="المحل / نقطة الانطلاق")
    driver = models.ForeignKey(CourierDriver, on_delete=models.SET_NULL, null=True, blank=True, related_name='dispatches', verbose_name="المندوب / السائق المعين")
    dispatch_type = models.CharField(max_length=20, choices=DISPATCH_TYPE_CHOICES, default='product', verbose_name="نوع المشوار")
    pickup_address = models.CharField(max_length=255, verbose_name="عنوان الاستلام")
    delivery_address = models.CharField(max_length=255, verbose_name="عنوان التسليم / الوجهة")
    fare = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="تكلفة التوصيل (جنيه)")
    status = models.CharField(max_length=50, default='in_transit', verbose_name="حالة المشوار")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الطلب")

    class Meta:
        verbose_name = "مهمة توصيل / مشوار"
        verbose_name_plural = "مهام التوصيل والمشاوير"

    def __str__(self):
        return f"مهمة #{self.id} ({self.get_dispatch_type_display()}) - {self.fare} ج.م"


class DeliveryZone(models.Model):
    name = models.CharField(max_length=255, verbose_name="اسم المنطقة")
    fee = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="رسوم التوصيل")

    class Meta:
        verbose_name = "منطقة توصيل"
        verbose_name_plural = "مناطق التوصيل"

    def __str__(self):
        return f"{self.name} - {self.fee} ج.م"


class SubscriptionPackage(models.Model):
    name = models.CharField(max_length=255, verbose_name="اسم الباقة")
    provider_type = models.CharField(max_length=50, choices=Store.PROVIDER_TYPE_CHOICES, default='restaurant_bakery', verbose_name="القطاع المستهدف")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="سعر الاشتراك")
    duration_days = models.IntegerField(default=30, verbose_name="مدة الباقة (بالأيام)")

    class Meta:
        verbose_name = "باقة اشتراك"
        verbose_name_plural = "باقات الاشتراكات"

    def __str__(self):
        return f"{self.name} ({self.price} ج.م)"


class ProviderSubscription(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='subscriptions', verbose_name="المزود / المحل")
    package = models.ForeignKey(SubscriptionPackage, on_delete=models.CASCADE, verbose_name="الباقة")
    start_date = models.DateField(auto_now_add=True, verbose_name="تاريخ البداية")
    end_date = models.DateField(verbose_name="تاريخ النهاية")
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="رصيد المحفظة (جنيه)")
    is_active = models.BooleanField(default=True, verbose_name="مفعل")

    class Meta:
        verbose_name = "اشتراك مزود"
        verbose_name_plural = "اشتراكات المزودين والمحفظة"

    def __str__(self):
        return f"اشتراك {self.store.name} - {self.package.name}"


class SMSCampaign(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True, blank=True, related_name='sms_campaigns', verbose_name="المزود المرسل")
    title = models.CharField(max_length=255, verbose_name="عنوان الحملة")
    message = models.TextField(verbose_name="نص الرسالة الدعائية")
    target_audience = models.CharField(max_length=255, verbose_name="الجمهور المستهدف")
    cost_per_sms = models.DecimalField(max_digits=5, decimal_places=2, default=0.75, verbose_name="سعر الرسالة (0.75 ج.م)")
    sent_count = models.PositiveIntegerField(default=0, verbose_name="عدد الرسائل المرسلة")
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="التكلفة الإجمالية (جنيه)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإطلاق")

    class Meta:
        verbose_name = "حملة رسائل SMS"
        verbose_name_plural = "حملات الرسائل الدعائية (0.75 ج.م)"

    def save(self, *args, **kwargs):
        self.total_cost = self.cost_per_sms * self.sent_count
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.sent_count} رسالة - {self.total_cost} ج.م)"
dels

class Store(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True, default='')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='menu_items', null=True, blank=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    description = models.TextField(blank=True, default='')

    def __str__(self):
        return self.name

class Addon(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='addons', null=True, blank=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name

class DeliveryZone(models.Model):
    name = models.CharField(max_length=255)
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name

class SubscriptionPackage(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name

class SMSCampaign(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField(blank=True, default='')
    sent_at = models.DateTimeFie

class FirstSectionConfig(models.Model):
    SECTOR_CHOICES = [
        ('restaurants_sweets', 'restaurants_sweets'),
        ('libraries_printing', 'libraries_printing'),
        ('realestate_finishing', 'realestate_finishing'),
        ('supermarket', 'supermarket'),
        ('map_transport', 'map_transport'),
        ('ai_assistant', 'ai_assistant'),
    ]

    sector_type = models.CharField(max_length=50, choices=SECTOR_CHOICES, unique=True, verbose_name="Sector Type")
    main_title = models.CharField(max_length=255, verbose_name="Main Title")
    description = models.TextField(blank=True, default='', verbose_name="Description")
    is_verified_badge = models.BooleanField(default=True, verbose_name="Verified Badge")
    quick_pinned_filters = models.CharField(max_length=255, blank=True, default='', verbose_name="Quick Pinned Filters")
    cta_button_text = models.CharField(max_length=100, blank=True, default='', verbose_name="CTA Button Text")
    cta_button_link = models.CharField(max_length=255, blank=True, default='', verbose_name="CTA Button Link")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")

    class Meta:
        verbose_name = "First Section Config"
        verbose_name_plural = "First Section Configs"

    def __str__(self):
        return f"{self.sector_type} - {self.main_title}"


class ConnectedEmailAccount(models.Model):
    email_address = models.EmailField(unique=True, verbose_name="Email Address")
    smtp_host = models.CharField(max_length=255, default='smtp.hostinger.com', verbose_name="SMTP Host")
    smtp_port = models.IntegerField(default=465, verbose_name="SMTP Port")
    smtp_user = models.CharField(max_length=255, verbose_name="SMTP User")
    smtp_password = models.CharField(max_length=255, verbose_name="SMTP Password")
    use_tls = models.BooleanField(default=False, verbose_name="Use TLS")
    use_ssl = models.BooleanField(default=True, verbose_name="Use SSL")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")

    class Meta:
        verbose_name = "Connected Email Account"
        verbose_name_plural = "Connected Email Accounts"

    def __str__(self):
        return f"{self.email_address} ({self.smtp_host}:{self.smtp_port})"


class UnifiedNotificationDispatch(models.Model):
    DISPATCH_CHOICES = [
        ('email', 'Email Only'),
        ('email_and_sms', 'Email + SMS'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
    ]

    sender_email = models.ForeignKey(ConnectedEmailAccount, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Sender Email")
    recipient = models.CharField(max_length=255, verbose_name="Recipient Email")
    phone_number = models.CharField(max_length=50, blank=True, default='', verbose_name="Phone Number")
    dispatch_type = models.CharField(max_length=20, choices=DISPATCH_CHOICES, default='email', verbose_name="Dispatch Type")
    title = models.CharField(max_length=255, verbose_name="Notification Title")
    message = models.TextField(verbose_name="Message Content")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Status")
    sent_at = models.DateTimeField(auto_now_add=True, verbose_name="Sent At")
    error_log = models.TextField(blank=True, default='', verbose_name="Error Log")

    class Meta:
        verbose_name = "Unified Notification Dispatch"
        verbose_name_plural = "Unified Notification Dispatches"

    def __str__(self):
        return f"{self.title} -> {self.recipient} [{self.status}]"

    def dispatch(self):
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        if not self.sender_email:
            self.status = 'failed'
            self.error_log = 'No connected sender email selected.'
            self.save()
            return False

        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email.email_address
            msg['To'] = self.recipient
            msg['Subject'] = self.title
            msg.attach(MIMEText(self.message, 'plain', 'utf-8'))

            if self.sender_email.use_ssl:
                server = smtplib.SMTP_SSL(self.sender_email.smtp_host, self.sender_email.smtp_port, timeout=10)
            else:
                server = smtplib.SMTP(self.sender_email.smtp_host, self.sender_email.smtp_port, timeout=10)
                if self.sender_email.use_tls:
                    server.starttls()

            if self.sender_email.smtp_user and self.sender_email.smtp_password:
                server.login(self.sender_email.smtp_user, self.sender_email.smtp_password)

            server.sendmail(self.sender_email.email_address, [self.recipient], msg.as_string())
            server.quit()

            self.status = 'sent'
            self.error_log = 'Sent successfully via SMTP'
            if self.dispatch_type == 'email_and_sms':
                self.error_log += ' | SMS dispatch triggered'
            self.save()
            return True
        except Exception as e:
            self.status = 'failed'
            self.error_log = f'SMTP Error: {str(e)}'
            self.save()
            return False


class MobileDeviceSession(models.Model):
    device_brand = models.CharField(max_length=100, default='Apple iPhone', verbose_name="Device Brand & Model")
    os_type = models.CharField(max_length=50, default='iOS', verbose_name="OS Type")
    open_path = models.CharField(max_length=255, default='/', verbose_name="Open Path")
    ip_address = models.CharField(max_length=50, blank=True, default='', verbose_name="IP Address")
    user_agent = models.TextField(blank=True, default='', verbose_name="User Agent")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Visit Time")

    class Meta:
        verbose_name = "Mobile Device Session"
        verbose_name_plural = "Mobile Device Sessions"

    def __str__(self):
        return f"{self.device_brand} ({self.os_type}) - {self.open_path}"


class MigratedUserVault(models.Model):
    full_name = models.CharField(max_length=255, verbose_name="Full Name")
    phone_number = models.CharField(max_length=50, verbose_name="Phone Number")
    role = models.CharField(max_length=50, default='Customer', verbose_name="Role")
    area = models.CharField(max_length=100, blank=True, default='', verbose_name="Area")
    past_orders_data = models.TextField(blank=True, default='[]', verbose_name="Past Orders Data (JSON)")
    raw_migration_data = models.TextField(blank=True, default='{}', verbose_name="Raw Migration Data (JSON)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Migration Date")

    class Meta:
        verbose_name = "Migrated User Vault"
        verbose_name_plural = "Migrated User Vaults"

    def __str__(self):
        return f"{self.full_name} ({self.phone_number}) - {self.role}"


    def __str__(self):
        return self.title
