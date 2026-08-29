
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-@temp-key-change-it'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
#    'unfold',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_jalali',
    'personnel',
    'warehouse',
    'projects',
    'tickets',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware', 
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'it_system.urls'

TEMPLATES = [{
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
}]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

LANGUAGE_CODE = 'fa'
TIME_ZONE = 'Asia/Tehran'
USE_I18N = True
USE_TZ = True
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

UNFOLD = {
    "SITE_TITLE": "مدیریت سیستم",
    "SITE_HEADER": "مدیریت سیستم",
    "SITE_URL": "/",
    "SITE_ICON": None,
    "SHOW_HISTORY": True,
    "THEME": "dark",
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": _("پرسنل"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {"title": _("بخش‌ها"), "link": reverse_lazy("admin:personnel_department_changelist")},
                    {"title": _("پرسنل‌ها"), "link": reverse_lazy("admin:personnel_personnel_changelist")},
                ],
            },
            {
                "title": _("پروژه‌ها"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {"title": _("پروژه‌ها"), "link": reverse_lazy("admin:projects_project_changelist")},
                ],
            },
            {
                "title": _("انبار"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {"title": _("دارایی‌ها"), "link": reverse_lazy("admin:warehouse_asset_changelist")},
                ],
            },
            {
                "title": _("تیکت‌ها"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {"title": _("تیکت‌ها"), "link": reverse_lazy("admin:tickets_ticket_changelist")},
                ],
            },
        ],
    },
}
