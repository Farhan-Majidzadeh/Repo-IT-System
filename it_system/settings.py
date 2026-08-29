from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-@temp-key-change-it'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'unfold',
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

# Force Persian language for all users
LANGUAGE_COOKIE_NAME = 'django_language'
LANGUAGE_COOKIE_AGE = 60 * 60 * 24 * 365  # 1 year

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

UNFOLD = {
    "SITE_TITLE": "مدیریت سیستم IT",
    "SITE_HEADER": "سیستم مدیریت IT",
    "SITE_SUBHEADER": "پنل مدیریت جامع",
    "SITE_URL": "/",
    "SITE_SYMBOL": "settings",
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": False,
    "THEME": "dark",
    "COLORS": {
        "primary": {
            "50": "250 245 255",
            "100": "244 231 255",
            "200": "238 217 255",
            "300": "224 186 255",
            "400": "206 147 255",
            "500": "187 107 255",
            "600": "168 85 247",
            "700": "147 51 234",
            "800": "126 34 206",
            "900": "107 27 183",
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": [
            {
                "title": _("پرسنل"),
                "icon": "people",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("بخش‌ها"),
                        "icon": "business",
                        "link": reverse_lazy("admin:personnel_department_changelist"),
                    },
                    {
                        "title": _("پرسنل‌ها"),
                        "icon": "badge",
                        "link": reverse_lazy("admin:personnel_personnel_changelist"),
                    },
                    {
                        "title": _("ارتباط پرسنل با بخش"),
                        "icon": "link",
                        "link": reverse_lazy("admin:personnel_personneldepartment_changelist"),
                    },
                ],
            },
            {
                "title": _("پروژه‌ها"),
                "icon": "folder_special",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("پروژه‌ها"),
                        "icon": "folder",
                        "link": reverse_lazy("admin:projects_project_changelist"),
                    },
                ],
            },
            {
                "title": _("انبار"),
                "icon": "warehouse",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("انبارها"),
                        "icon": "inventory_2",
                        "link": reverse_lazy("admin:warehouse_warehouse_changelist"),
                    },
                    {
                        "title": _("دارایی‌ها"),
                        "icon": "devices",
                        "link": reverse_lazy("admin:warehouse_asset_changelist"),
                    },
                    {
                        "title": _("تحویل دارایی"),
                        "icon": "handshake",
                        "link": reverse_lazy("admin:warehouse_assetdelivery_changelist"),
                    },
                ],
            },
            {
                "title": _("تیکت‌ها"),
                "icon": "confirmation_number",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("تیکت‌ها"),
                        "icon": "ticket",
                        "link": reverse_lazy("admin:tickets_ticket_changelist"),
                    },
                    {
                        "title": _("دسته‌بندی تیکت‌ها"),
                        "icon": "category",
                        "link": reverse_lazy("admin:tickets_ticketcategory_changelist"),
                    },
                    {
                        "title": _("تخصیص‌ها"),
                        "icon": "assignment_ind",
                        "link": reverse_lazy("admin:tickets_assignment_changelist"),
                    },
                    {
                        "title": _("پیام‌های تیکت"),
                        "icon": "chat",
                        "link": reverse_lazy("admin:tickets_ticketmessage_changelist"),
                    },
                ],
            },
            {
                "title": _("مدیریت کاربران"),
                "icon": "admin_panel_settings",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("کاربران"),
                        "icon": "people",
                        "link": reverse_lazy("admin:auth_user_changelist"),
                    },
                    {
                        "title": _("گروه‌ها"),
                        "icon": "group",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                    },
                ],
            },
        ],
    },
    "TABS": [],
}
