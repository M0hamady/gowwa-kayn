import uuid
from django.utils.deprecation import MiddlewareMixin
from core.models import MobileDeviceAnalytics

class MobileDeviceAnalyticsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        ip_address = request.META.get('REMOTE_ADDR', '127.0.0.1')
        endpoint = request.path
        
        is_mobile = any(kw in user_agent.lower() for kw in ['mobile', 'android', 'iphone', 'ipad'])
        if is_mobile:
            device_uuid = request.COOKIES.get('jowwa_device_id') or str(uuid.uuid4())[:32]
            try:
                analytics, _ = MobileDeviceAnalytics.objects.get_or_create(
                    device_uuid=device_uuid,
                    defaults={
                        'user_agent': user_agent[:255],
                        'ip_address': ip_address[:45],
                        'last_endpoint': endpoint[:255]
                    }
                )
                analytics.user_agent = user_agent[:255]
                analytics.ip_address = ip_address[:45]
                analytics.last_endpoint = endpoint[:255]
                analytics.save()
            except Exception:
                pass

class SecurityHeadersAndAuditMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['X-Jowwa-Encryption-Audit'] = 'PBKDF2-HMAC-SHA256-Active'
        return response
