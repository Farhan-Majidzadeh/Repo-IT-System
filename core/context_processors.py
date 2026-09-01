"""
Context processor for SiteSettings - provides site settings to all templates.
"""
from .models import SiteSettings


def site_settings_context(request):
    """اضافه کردن تنظیمات سایت به همه template ها"""
    try:
        settings = SiteSettings.get_instance()
        return {
            'site_settings': settings,
            'site_css': settings.get_dynamic_css(),
        }
    except Exception:
        return {
            'site_settings': None,
            'site_css': '',
        }
