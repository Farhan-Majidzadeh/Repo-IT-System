from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from .models import CredentialCategory, Credential, CredentialAccess, CredentialLog


@admin.register(CredentialCategory)
class CredentialCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category_type', 'icon', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    list_filter = ['category_type', 'is_active']
    search_fields = ['name', 'description']
    list_per_page = 20


class CredentialAccessInline(admin.TabularInline):
    model = CredentialAccess
    extra = 0
    fields = ['user', 'group', 'access_level', 'note']
    autocomplete_fields = ['user', 'group']


@admin.register(Credential)
class CredentialAdmin(admin.ModelAdmin):
    list_display = [
        'title_badge', 'category', 'branch', 'hostname_display',
        'username', 'security_level_badge', 'status_badge',
        'access_count', 'updated_at',
    ]
    list_filter = [
        'category', 'branch', 'security_level', 'status',
    ]
    search_fields = ['title', 'hostname', 'username', 'domain', 'notes']
    readonly_fields = ['created_by', 'created_at', 'updated_at', 'password_display']
    inlines = [CredentialAccessInline]
    list_per_page = 25
    fieldsets = (
        (_('اطلاعات اصلی'), {
            'fields': ('title', 'category', 'branch', 'status', 'security_level'),
        }),
        (_('اطلاعات اتصال'), {
            'fields': ('hostname', 'port', 'url'),
        }),
        (_('اطلاعات کاربری'), {
            'fields': ('username', 'password_encrypted', 'email', 'domain'),
        }),
        (_('تاریخچه رمز'), {
            'fields': ('last_password_change', 'password_expiry', 'password_display'),
            'classes': ('collapse',),
        }),
        (_('یادداشت‌ها'), {
            'fields': ('notes',),
            'classes': ('collapse',),
        }),
        (_('فراداده'), {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def title_badge(self, obj):
        colors = {
            'critical': '#ef4444',
            'high': '#f97316',
            'medium': '#eab308',
            'low': '#22c55e',
        }
        color = colors.get(obj.security_level, '#6b7280')
        return format_html(
            '<span style="border-right:3px solid {}; padding-right:8px; font-weight:bold;">{}</span>',
            color, obj.title
        )
    title_badge.short_description = _('عنوان')

    def hostname_display(self, obj):
        if obj.hostname:
            port = f":{obj.port}" if obj.port else ""
            return format_html('<code style="background:#1e1e2e; padding:2px 6px; border-radius:4px;">{}{}</code>', obj.hostname, port)
        return '-'
    hostname_display.short_description = _('آدرس')

    def security_level_badge(self, obj):
        badges = {
            'low': '<span style="background:#22c55e22; color:#22c55e; padding:2px 8px; border-radius:12px; font-size:11px;">🟢 عادی</span>',
            'medium': '<span style="background:#eab30822; color:#eab308; padding:2px 8px; border-radius:12px; font-size:11px;">🟡 متوسط</span>',
            'high': '<span style="background:#f9731622; color:#f97316; padding:2px 8px; border-radius:12px; font-size:11px;">🟠 حساس</span>',
            'critical': '<span style="background:#ef444422; color:#ef4444; padding:2px 8px; border-radius:12px; font-size:11px;">🔴 بحرانی</span>',
        }
        return format_html(badges.get(obj.security_level, ''))
    security_level_badge.short_description = _('سطح امنیت')

    def status_badge(self, obj):
        badges = {
            'active': '<span style="background:#22c55e22; color:#22c55e; padding:2px 8px; border-radius:12px;">فعال</span>',
            'inactive': '<span style="background:#6b728022; color:#9ca3af; padding:2px 8px; border-radius:12px;">غیرفعال</span>',
            'expired': '<span style="background:#ef444422; color:#ef4444; padding:2px 8px; border-radius:12px;">منقضی</span>',
            'archived': '<span style="background:#3b82f622; color:#3b82f6; padding:2px 8px; border-radius:12px;">بایگانی</span>',
        }
        return format_html(badges.get(obj.status, ''))
    status_badge.short_description = _('وضعیت')

    def access_count(self, obj):
        count = obj.access_entries.count()
        return format_html('<span style="background:#3b82f622; color:#3b82f6; padding:2px 8px; border-radius:12px;">{} نفر</span>', count)
    access_count.short_description = _('دسترسی')

    def password_display(self, obj):
        if obj.password_encrypted:
            return format_html(
                '<code style="background:#1e1e2e; padding:4px 8px; border-radius:4px; color:#a78bfa;">••••••••</code> '
                '<small style="color:#6b7280;">رمزنگاری شده با Django Signer</small>'
            )
        return '-'
    password_display.short_description = _('وضعیت رمز')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    class Media:
        js = ('admin/js/credential_admin.js',)


@admin.register(CredentialAccess)
class CredentialAccessAdmin(admin.ModelAdmin):
    list_display = ['credential', 'user_display', 'group_display', 'access_level_badge', 'granted_by', 'granted_at']
    list_filter = ['access_level', 'credential__category', 'credential__branch']
    search_fields = [
        'credential__title', 'user__username', 'user__first_name',
        'user__last_name', 'group__name',
    ]
    autocomplete_fields = ['credential', 'user', 'group']
    list_per_page = 30

    def user_display(self, obj):
        if obj.user:
            name = obj.user.get_full_name() or obj.user.username
            return format_html('<span style="color:#a78bfa;">👤 {}</span>', name)
        return '-'
    user_display.short_description = _('کاربر')

    def group_display(self, obj):
        if obj.group:
            return format_html('<span style="color:#60a5fa;">👥 {}</span>', obj.group.name)
        return '-'
    group_display.short_description = _('گروه')

    def access_level_badge(self, obj):
        badges = {
            'view': '<span style="background:#3b82f622; color:#3b82f6; padding:2px 8px; border-radius:12px;">👁 مشاهده</span>',
            'copy': '<span style="background:#22c55e22; color:#22c55e; padding:2px 8px; border-radius:12px;">📋 مشاهده+کپی</span>',
            'edit': '<span style="background:#f9731622; color:#f97316; padding:2px 8px; border-radius:12px;">✏️ ویرایش</span>',
            'full': '<span style="background:#ef444422; color:#ef4444; padding:2px 8px; border-radius:12px;">🔑 کامل</span>',
        }
        return format_html(badges.get(obj.access_level, ''))
    access_level_badge.short_description = _('سطح دسترسی')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.granted_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(CredentialLog)
class CredentialLogAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'credential', 'user', 'access_type_badge', 'ip_address']
    list_filter = ['access_type', 'credential__category', 'credential__branch']
    search_fields = ['credential__title', 'user__username', 'ip_address']
    readonly_fields = ['credential', 'user', 'access_type', 'ip_address', 'user_agent', 'details', 'created_at']
    list_per_page = 50

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def access_type_badge(self, obj):
        badges = {
            'view': '<span style="color:#3b82f6;">👁️ مشاهده</span>',
            'copy_password': '<span style="color:#22c55e;">📋 کپی رمز</span>',
            'edit': '<span style="color:#f97316;">✏️ ویرایش</span>',
            'create': '<span style="color:#a78bfa;">➕ ایجاد</span>',
            'delete': '<span style="color:#ef4444;">🗑️ حذف</span>',
            'grant_access': '<span style="color:#60a5fa;">🔑 اعطای دسترسی</span>',
            'revoke_access': '<span style="color:#ef4444;">🔒 لغو دسترسی</span>',
        }
        return format_html(badges.get(obj.access_type, obj.access_type))
    access_type_badge.short_description = _('نوع')
