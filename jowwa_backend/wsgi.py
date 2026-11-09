import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path: sys.path.insert(0, BASE_DIR)
    import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jowwa_backend.settings')

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
app = application

try:
    from django.core.management import call_command
    from django.contrib.auth import get_user_model

    call_command('migrate', '--run-syncdb', interactive=False)

    User = get_user_model()
    if not User.objects.filter(username='jowwa_admin').exists():
        User.objects.create_superuser('jowwa_admin', 'admin@gowwa.com', 'Jowwa@Admin2026!')

    from core.models import Store, MenuItem, DeliveryZone, SubscriptionPackage, SMSCampaign
    if not Store.objects.exists():
        Store.objects.create(name='مطعم جوة كاين', is_active=True)
    if not DeliveryZone.objects.exists():
        DeliveryZone.objects.create(name='القاهرة', fee=25.00)
    if not SubscriptionPackage.objects.exists():
        SubscriptionPackage.objects.create(name='الباقة الأساسية', price=100.00)
    if not SMSCampaign.objects.exists():
        SMSCampaign.objects.create(title='ترحيب', message='مرحباً بكم في جوة كاين')
except Exception as e:
    print(f"WSGI DB init error: {e}")

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jowwa_backend.settings')

application = get_wsgi_application()

try:
    from django.core.management import call_command
    from django.contrib.auth import get_user_model
    from core.models import Store, MenuItem, Addon, DeliveryZone, SubscriptionPackage, SMSCampaign

    call_command('migrate', '--run-syncdb', interactive=False)

    User = get_user_model()
    if not User.objects.filter(username='jowwa_admin').exists():
        User.objects.create_superuser('jowwa_admin', 'm0ham3dy96@gmail.com', 'Jowwa@Admin2026!')

    if not Store.objects.exists():
        sucreve = Store.objects.create(
            name='Sucréve',
            priority=1,
            is_verified=True,
            badge='شريك موثّق',
            category='حلويات وسينابون',
            description='أشهر واجهة للسينابون والإضافات الفاخرة'
        )
        DeliveryZone.objects.create(store=sucreve, zone_name='كرمة 1', price=25.00)
        DeliveryZone.objects.create(store=sucreve, zone_name='كرمة 2', price=35.00)

        c1 = MenuItem.objects.create(store=sucreve, name='سينابون كلاسيك رول', price=65.00, description='رول القرفة الأصلي الصوص الكلاسيكي')
        c2 = MenuItem.objects.create(store=sucreve, name='سينابون شوكولاتة ونوتيلا', price=75.00, description='رول القرفة مغطى بصوص النوتيلا الغني')
        c3 = MenuItem.objects.create(store=sucreve, name='سينابون لوتس كراميل', price=80.00, description='رول القرفة مع بوبس اللوتس وزبدة الكراميل')

        Addon.objects.create(menu_item=c1, name='إضافة صوص كراميل إضافي', price=15.00)
        Addon.objects.create(menu_item=c1, name='إضافة صوص جبنة كلاسيك', price=20.00)
        Addon.objects.create(menu_item=c1, name='إضافة مكسرات عين جمل', price=25.00)
        Addon.objects.create(menu_item=c2, name='إضافة قطع شوكولاتة كيندر', price=25.00)

        Store.objects.create(name='صان مول', priority=2, is_verified=False, badge='', category='سوبر ماركت ومول', description='تسوق جميع المنتجات والسلع الغذائية')
        Store.objects.create(name='كشري العمدة', priority=3, is_verified=True, badge='شريك موثّق', category='مطاعم ومأكولات شعبية', description='أطيب وألذ أطباق الكشري المصري الأصيل')
        Store.objects.create(name='مطبعة كيان سيتي', priority=4, is_verified=False, badge='', category='خدمات وطباعة', description='خدمات الطباعة الرقمية والدعاية والإعلان')

        SubscriptionPackage.objects.create(name='باقة البداية', price=299.00, duration='شهرية', sms_included=200, price_per_sms=0.75, features='لوحة تحكم + 200 رسالة SMS')
        SubscriptionPackage.objects.create(name='باقة النمو الاحترافية', price=599.00, duration='شهرية', sms_included=1000, price_per_sms=0.75, features='منظومة المطبخ + 1000 رسالة SMS + دعم أولوية')
        SubscriptionPackage.objects.create(name='باقة التاجر الذهبية', price=999.00, duration='سنوية', sms_included=3000, price_per_sms=0.75, features='ربط شامل + شارة شريك موثق + 3000 رسالة')

        SMSCampaign.objects.create(name='حملة عروض الجمعة لعملاء Sucréve', store_name='Sucréve', target_audience='عملاء منطقة كرمة 1 و 2', recipient_count=500, price_per_sms=0.75, total_cost=375.00, status='نشطة')
except Exception as e:
    print("Auto-init exception:", e)
