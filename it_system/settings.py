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
    'reports',
    'core',
    'credentials',
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
            'core.context_processors.site_settings_context',
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

LANGUAGE_COOKIE_NAME = 'django_language'
LANGUAGE_COOKIE_AGE = 60 * 60 * 24 * 365

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_DIRS = [
    BASE_DIR / 'staticfiles',
]

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
                "title": _("\u06af\u0632\u0627\u0631\u0634"),
                "icon": "dashboard",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("\u062f\u0627\u0634\u0628\u0648\u0631\u062f"),
                        "icon": "analytics",
                        "link": "/reports/dashboard/",
                    },
                ],
            },
            {
                "title": _("\u0634\u0639\u0628\u0647\u200c\u0647\u0627"),
                "icon": "apartment",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("\u0634\u0639\u0628\u0647\u200c\u0647\u0627"),
                        "icon": "location_city",
                        "link": reverse_lazy("admin:personnel_branch_changelist"),
                    },
                ],
            },
            {
                "title": _("\u067e\u0631\u0633\u0646\u0644"),
                "icon": "people",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("\u0628\u062e\u0634\u200c\u0647\u0627"),
                        "icon": "business",
                        "link": reverse_lazy("admin:personnel_department_changelist"),
                    },
                    {
                        "title": _("\u067e\u0631\u0633\u0646\u0644\u200c\u0647\u0627"),
                        "icon": "badge",
                        "link": reverse_lazy("admin:personnel_personnel_changelist"),
                    },
                    {
                        "title": _("\u0627\u0631\u062a\u0628\u0627\u0637 \u067e\u0631\u0633\u0646\u0644 \u0628\u0627 \u0628\u062e\u0634"),
                        "icon": "link",
                        "link": reverse_lazy("admin:personnel_personneldepartment_changelist"),
                    },
                ],
            },
            {
                "title": _("\u062a\u0623\u0645\u06cc\u0646\u200c\u06a9\u0646\u0646\u062f\u06af\u0627\u0646"),
                "icon": "local_shipping",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("\u062a\u0623\u0645\u06cc\u0646\u200c\u06a9\u0646\u0646\u062f\u06af\u0627\u0646"),
                        "icon": "store",
                        "link": reverse_lazy("admin:warehouse_supplier_changelist"),
                    },
                ],
            },
            {
                "title": _("\u0627\u0646\u0628\u0627\u0631"),
                "icon": "warehouse",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("\u0627\u0646\u0628\u0627\u0631\u0647\u0627"),
                        "icon": "inventory_2",
                        "link": reverse_lazy("admin:warehouse_warehouse_changelist"),
                    },
                    {
                        "title": _("\u062f\u0627\u0631\u0627\u06cc\u06cc\u200c\u0647\u0627"),
                        "icon": "devices",
                        "link": reverse_lazy("admin:warehouse_asset_changelist"),
                    },
                    {
                        "title": _("\u06a9\u0627\u0631\u062a\u0631\u06cc\u062c\u200c\u0647\u0627"),
                        "icon": "print",
                        "link": reverse_lazy("admin:warehouse_cartridgecharge_changelist"),
                    },
                    {
                        "title": _("\u0647\u0632\u06cc\u0646\u0647\u200c\u0647\u0627 \u0648 \u0645\u0635\u0631\u0641\u06cc\u0627\u062a"),
                        "icon": "construction",
                        "link": reverse_lazy("admin:warehouse_assetreferral_changelist"),
                    },
                    {
                        "title": _("\u062a\u062d\u0648\u06cc\u0644 \u062f\u0627\u0631\u0627\u06cc\u06cc"),
                        "icon": "handshake",
                        "link": reverse_lazy("admin:warehouse_assetdelivery_changelist"),
                    },
                ],
            },
            {
                "title": _("\u062a\u06cc\u06a9\u062a\u200c\u0647\u0627"),
                "icon": "confirmation_number",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("\u062a\u06cc\u06a9\u062a\u200c\u0647\u0627"),
                        "icon": "ticket",
                        "link": reverse_lazy("admin:tickets_ticket_changelist"),
                    },
                    {
                        "title": _("\u062f\u0633\u062a\u0647\u200c\u0628\u0646\u062f\u06cc \u062a\u06cc\u06a9\u062a\u200c\u0647\u0627"),
                        "icon": "category",
                        "link": reverse_lazy("admin:tickets_ticketcategory_changelist"),
                    },
                    {
                        "title": _("\u062a\u062e\u0635\u06cc\u0635\u200c\u0647\u0627"),
                        "icon": "assignment_ind",
                        "link": reverse_lazy("admin:tickets_assignment_changelist"),
                    },
                    {
                        "title": _("\u067e\u06cc\u0627\u0645\u200c\u0647\u0627\u06cc \u062a\u06cc\u06a9\u062a"),
                        "icon": "chat",
                        "link": reverse_lazy("admin:tickets_ticketmessage_changelist"),
                    },
                ],
            },
            {
                "title": _("\u06af\u0632\u0627\u0631\u0634\u200c\u06af\u06cc\u0631\u06cc"),
                "icon": "assessment",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("\u06af\u0632\u0627\u0631\u0634 \u062a\u062c\u0647\u06cc\u0632\u0627\u062a"),
                        "icon": "inventory",
                        "link": "/reports/assets/",
                    },
                    {
                        "title": _("\u06af\u0632\u0627\u0631\u0634 \u06a9\u0627\u0644\u0627\u0647\u0627\u06cc \u0645\u0635\u0631\u0641\u06cc"),
                        "icon": "local_mall",
                        "link": "/reports/consumables/",
                    },
                    {
                        "title": _("\u06af\u0632\u0627\u0631\u0634 \u0634\u0627\u0631\u0698 \u06a9\u0627\u0631\u062a\u0631\u06cc\u062c"),
                        "icon": "print",
                        "link": "/reports/cartridges/",
                    },
                    {
                        "title": _("\u06af\u0632\u0627\u0631\u0634 \u0627\u0631\u062c\u0627\u0639\u0627\u062a"),
                        "icon": "build",
                        "link": "/reports/referrals/",
                    },
                    {
                        "title": _("\u06af\u0632\u0627\u0631\u0634 \u062a\u06cc\u06a9\u062a\u200c\u0647\u0627"),
                        "icon": "analytics",
                        "link": "/reports/tickets/",
                    },
                ],
            },
            {
                "title": _("\u0645\u062f\u06cc\u0631\u06cc\u062a \u0627\u0637\u0644\u0627\u0639\u0627\u062a \u062f\u0633\u062a\u0631\u0633\u06cc"),
                "icon": "vpn_key",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("\u062f\u0633\u062a\u0647 \u200c\u0647\u0627"),
                        "icon": "vpn_key",
                        "link": reverse_lazy("admin:credentials_credential_changelist"),
                    },
                    {
                        "title": _("\u062f\u0633\u062a\u0647 \u200c\u0647\u0627"),
                        "icon": "category",
                        "link": reverse_lazy("admin:credentials_credentialcategory_changelist"),
                    },
                    {
                        "title": _("\u062f\u0633\u062a\u0631\u0633\u06cc \u200c\u0647\u0627"),
                        "icon": "admin_panel_settings",
                        "link": reverse_lazy("admin:credentials_credentialaccess_changelist"),
                    },
                    {
                        "title": _("\u0644\u0627\u06af \u062f\u0633\u062a\u0631\u0633\u06cc"),
                        "icon": "history",
                        "link": reverse_lazy("admin:credentials_credentiallog_changelist"),
                    },
                ],
            },
            {
                "title": _("\u0645\u062f\u06cc\u0631\u06cc\u062a \u06a9\u0627\u0631\u0628\u0631\u0627\u0646"),
                "icon": "admin_panel_settings",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("\u06a9\u0627\u0631\u0628\u0631\u0627\u0646"),
                        "icon": "people",
                        "link": reverse_lazy("admin:auth_user_changelist"),
                    },
                    {
                        "title": _("\u06af\u0631\u0648\u0647\u200c\u0647\u0627"),
                        "icon": "group",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                    },
                ],
            },
            {
                "title": _("\u062a\u0639\u0635\u06cc\u0645\u0627\u062a \u0633\u0627\u06cc\u062a"),
                "icon": "tune",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("\u062a\u0639\u0635\u06cc\u0645\u0627\u062a \u0638\u0627\u0647\u0631\u06cc"),
                        "icon": "palette",
                        "link": "/admin/core/sitesettings/1/change/",
                    },
                ],
            },
        ],
    },
    "TABS": [],
    "SCRIPTS": [
        lambda request: '/static/admin/js/custom_admin.js',
    ],
    "STYLES": [
        lambda request: '/static/admin/css/custom_admin.css',
        lambda request: '/static/admin/css/rtl_unfold.css',
    ],
}
