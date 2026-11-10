import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Dynamic App Generation in /tmp/jowwa_apps/
TMP_APPS_DIR = "/tmp/jowwa_apps"
os.makedirs(TMP_APPS_DIR, exist_ok=True)
if TMP_APPS_DIR not in sys.path:
    sys.path.insert(0, TMP_APPS_DIR)

APPS_CONFIG = {
    'accounts_roles': 'إدارة الحسابات والأدوار',
    'hero_customizer': 'تخصيص الهيرو والواجهة',
    'stores_pos': 'المحلات ونقاط البيع',
    'printing_libraries': 'الطباعة والمكتبات',
    'realestate_finishing': 'العقارات والتشطيبات',
    'map_geo': 'الخرائط والمواقع الجغرافية',
    'transit_hub': 'مواقف الباصات والقطارات والمناديب',
    'ai_assistant': 'مساعد الذكاء الاصطناعي - اسأل جوه',
    'services_directory': 'دليل الخدمات العامة',
    'subscriptions_sms': 'الاشتراكات وحملات الرسائل',
    'notifications_mailer': 'الإشعارات وربط الإيميلات',
    'device_analytics': 'تحليلات الأجهزة والخزنة',
}

for app_name, verbose_name in APPS_CONFIG.items():
    app_dir = os.path.join(TMP_APPS_DIR, app_name)
    os.makedirs(app_dir, exist_ok=True)
    init_file = os.path.join(app_dir, '__init__.py')
    if not os.path.exists(init_file):
        with open(init_file, 'w', encoding='utf-8') as f:
            f.write('')
    class_name = "".join([word.capitalize() for word in app_name.split("_")]) + "Config"
    apps_file = os.path.join(app_dir, 'apps.py')
    apps_content = f"""from django.apps import AppConfig

class {class_name}(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = '{app_name}'
    verbose_name = '{verbose_name}'
"""
    with open(apps_file, 'w', encoding='utf-8') as f:
        f.write(apps_content)

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-jowwa-kayn-secret-key-2026-production')
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'core',
    'accounts_roles',
    'hero_customizer',
    'stores_pos',
    'printing_libraries',
    'realestate_finishing',
    'map_geo',
    'transit_hub',
    'ai_assistant',
    'services_directory',
    'subscriptions_sms',
    'notifications_mailer',
    'device_analytics',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.MobileDeviceAnalyticsMiddleware',
    'core.middleware.SecurityHeadersAndAuditMiddleware',
]

ROOT_URLCONF = 'jowwa_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'jowwa_backend.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/tmp/jowwa_v8.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'ar-eg'
TIME_ZONE = 'Africa/Cairo'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOW_ALL_ORIGINS = True
