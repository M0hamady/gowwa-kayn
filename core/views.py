from django.http import HttpResponse, JsonResponse
from .models import Store, MenuItem, Addon, DeliveryZone, SubscriptionPackage, SMSCampaign

def home_view(request):
    html = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>منصة جوة كاين | Gowwa Kayn Platform</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f8f9fa; color: #333; margin: 0; padding: 40px; text-align: center; }
        .container { max-width: 800px; margin: 0 auto; background: #ffffff; padding: 40px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
        h1 { color: #2c3e50; margin-bottom: 10px; }
        p { font-size: 1.1rem; color: #666; }
        .links { margin-top: 30px; display: flex; justify-content: center; gap: 20px; }
        .btn { display: inline-block; padding: 12px 24px; background: #0070f3; color: white; text-decoration: none; border-radius: 6px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h1>منصة جوة كاين | Gowwa Kayn</h1>
        <p>نظام إدارة المتاجر والطلبات والحملات الإعلانية</p>
        <div class="links">
            <a class="btn" href="/admin/">لوحة التحكم (Django Admin)</a>
            <a class="btn" href="/api/v1/">واجهة الـ API (/api/v1/)</a>
        </div>
    </div>
</body>
</html>"""
    return HttpResponse(html)

def api_root_view(request):
    return JsonResponse({
        "status": "success",
        "message": "Gowwa Kayn API v1 Working",
        "endpoints": {
            "stores": "/api/v1/stores/",
            "subscriptions": "/api/v1/subscriptions/",
            "campaigns": "/api/v1/campaigns/",
            "orders": "/api/v1/orders/",
            "admin": "/admin/"
        }
    })

def api_stores_view(request):
    stores = list(Store.objects.values('id', 'name', 'is_active', 'created_at'))
    return JsonResponse({"status": "success", "stores": stores})

def api_subscriptions_view(request):
    subs = list(SubscriptionPackage.objects.values('id', 'name', 'price'))
    return JsonResponse({"status": "success", "subscriptions": subs})

def api_campaigns_view(request):
    campaigns = list(SMSCampaign.objects.values('id', 'title', 'message', 'sent_at'))
    return JsonResponse({"status": "success", "campaigns": campaigns})

def api_orders_view(request):
    return JsonResponse({"status": "success", "orders": []})
