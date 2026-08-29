from django.contrib import admin
from django.utils.html import format_html
from django_jalali.admin.filters import JDateFieldListFilter
import django_jalali.admin as jadmin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'status_badge', 'start_date', 'end_date', 'ticket_count', 'created_at')
    search_fields = ('name', 'description')
    list_filter = (
        'status',
        ('start_date', JDateFieldListFilter),
    )
    readonly_fields = ('code', 'created_at')
    exclude = ('code',)
    fieldsets = (
        ('اطلاعات پروژه', {
            'fields': ('name', 'description'),
        }),
        ('تاریخ‌ها و وضعیت', {
            'fields': ('start_date', 'end_date', 'status'),
        }),
        ('تاریخچه', {
            'fields': ('code', 'created_at'),
            'classes': ('collapse',),
        }),
    )

    def status_badge(self, obj):
        colors = {
            'active': '#22c55e',
            'completed': '#3b82f6',
            'on_hold': '#f59e0b',
            'cancelled': '#ef4444',
        }
        labels = {
            'active': 'فعال',
            'completed': 'تکمیل شده',
            'on_hold': 'متوقف',
            'cancelled': 'لغو شده',
        }
        color = colors.get(obj.status, '#94a3b8')
        label = labels.get(obj.status, obj.status)
        return format_html(
            '<span style="background:{};color:white;padding:2px 8px;border-radius:12px;font-size:12px;">{}</span>',
            color, label
        )
    status_badge.short_description = 'وضعیت'

    def ticket_count(self, obj):
        count = obj.ticket_set.count()
        return format_html(
            '<span style="background:#6366f1;color:white;padding:2px 8px;border-radius:12px;font-size:12px;">{} تیکت</span>',
            count
        )
    ticket_count.short_description = 'تعداد تیکت'
