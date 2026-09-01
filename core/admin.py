from django.contrib import admin
from django.utils.html import format_html
from .models import SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('name', 'theme_badge', 'primary_color_badge', 'font_name', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('📝 اطلاعات سایت', {
            'fields': ('name', 'subheader'),
        }),
        ('🎨 ظاهر', {
            'fields': ('theme', 'primary_color', 'font', 'font_size', 'border_radius'),
        }),
        ('🔧 نمایش', {
            'fields': ('show_breadcrumbs', 'show_logo', 'sidebar_compact'),
        }),
        ('💻 CSS سفارشی', {
            'fields': ('custom_css',),
            'classes': ('collapse',),
        }),
        ('📅 تاریخچه', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def theme_badge(self, obj):
        if obj.theme == 'dark':
            return format_html('<span style="background:#1e1e2e;color:#cdd6f4;padding:4px 12px;border-radius:16px;font-size:12px;">🌙 تاریک</span>')
        return format_html('<span style="background:#eff6ff;color:#1e40af;padding:4px 12px;border-radius:16px;font-size:12px;">☀️ روشن</span>')
    theme_badge.short_description = 'تم'

    def primary_color_badge(self, obj):
        color_map = {
            'purple': ('#8b5cf6', 'بنفش'),
            'blue': ('#3b82f6', 'آبی'),
            'green': ('#22c55e', 'سبز'),
            'red': ('#ef4444', 'قرمز'),
            'orange': ('#f97316', 'نارنجی'),
            'teal': ('#14b8a6', 'سبزآبی'),
            'pink': ('#ec4899', 'صورتی'),
            'indigo': ('#6366f1', 'نیلی'),
        }
        color, name = color_map.get(obj.primary_color, ('#8b5cf6', 'بنفش'))
        return format_html('<span style="background:{};color:white;padding:4px 12px;border-radius:16px;font-size:12px;">● {}</span>', color, name)
    primary_color_badge.short_description = 'رنگ اصلی'

    def font_name(self, obj):
        return format_html('<span style="font-family:{};font-size:14px;">{}</span>', obj.get_font_family(), obj.get_font_display())
    font_name.short_description = 'فونت'

    def has_add_permission(self, request):
        # فقط یه رکورد تنظیمات وجود داشته باشه
        if SiteSettings.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # پاک کردن کش CSS
        from django.core.cache import cache
        cache.delete('site_settings_css')
