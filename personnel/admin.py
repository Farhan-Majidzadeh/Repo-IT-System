from django.contrib import admin
from django.utils.html import format_html
from .models import Department, Personnel, PersonnelDepartment


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'building', 'personnel_count', 'created_at')
    search_fields = ('code', 'name', 'building')
    list_filter = ('building',)
    readonly_fields = ('created_at',)
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('code', 'name', 'building'),
        }),
        ('تاریخچه', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )

    def personnel_count(self, obj):
        count = obj.personneldepartment_set.count()
        return format_html(
            '<span style="background:#6366f1;color:white;padding:2px 8px;border-radius:12px;font-size:12px;">{}</span>',
            count
        )
    personnel_count.short_description = 'تعداد پرسنل'


@admin.register(Personnel)
class PersonnelAdmin(admin.ModelAdmin):
    list_display = ('personnel_code', 'full_name', 'email', 'phone', 'entry_date', 'is_active', 'created_at')
    search_fields = ('personnel_code', 'full_name', 'email', 'phone')
    list_filter = ('is_active', 'entry_date')

    readonly_fields = ('created_at',)
    fieldsets = (
        ('اطلاعات شخصی', {
            'fields': ('personnel_code', 'full_name', 'email', 'phone'),
        }),
        ('اطلاعات استخدام', {
            'fields': ('entry_date', 'settlement_date', 'is_active'),
        }),
        ('تاریخچه', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )

    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html(
                '<span style="background:#22c55e;color:white;padding:2px 8px;border-radius:12px;font-size:12px;">فعال</span>'
            )
        return format_html(
            '<span style="background:#ef4444;color:white;padding:2px 8px;border-radius:12px;font-size:12px;">غیرفعال</span>'
        )
    is_active_badge.short_description = 'وضعیت'


@admin.register(PersonnelDepartment)
class PersonnelDepartmentAdmin(admin.ModelAdmin):
    list_display = ('personnel', 'department', 'entry_date', 'exit_date', 'is_current_badge')
    list_filter = ('is_current', 'department')
    search_fields = ('personnel__full_name', 'department__name')
    raw_id_fields = ('personnel', 'department')

    def is_current_badge(self, obj):
        if obj.is_current:
            return format_html(
                '<span style="background:#22c55e;color:white;padding:2px 8px;border-radius:12px;font-size:12px;">فعلی</span>'
            )
        return format_html(
            '<span style="background:#94a3b8;color:white;padding:2px 8px;border-radius:12px;font-size:12px;"> سابق</span>'
        )
    is_current_badge.short_description = 'وضعیت'
