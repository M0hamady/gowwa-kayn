from django.contrib import admin
from django.urls import path, include
from core.views import home_view, api_root_view, api_stores_view, api_subscriptions_view, api_campaigns_view, api_orders_view

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('api/v1/', api_root_view, name='api_root'),
    path('api/v1/stores/', api_stores_view, name='api_stores'),
    path('api/v1/subscriptions/', api_subscriptions_view, name='api_subscriptions'),
    path('api/v1/campaigns/', api_campaigns_view, name='api_campaigns'),
    path('api/v1/orders/', api_orders_view, name='api_orders'),
]
