from django.contrib import admin
from django.utils.html import format_html
from django_jalali.admin.filters import JDateFieldListFilter
import django_jalali.admin as jadmin
from .models import TicketCategory, Assignment, Ticket, TicketMessage


@admin.register(TicketCategory)
class TicketCategoryAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'level', 'parent', 'ticket_count', 'created_at')
    search_fields = ('title', 'path')
    list_filter = ('level',)
    readonly_fields = ('code', 'created_at')
    exclude = ('code',)
    fieldsets = (
        ('اطلاعات دسته‌بندی', {
            'fields': ('title', 'parent'),
        }),
        ('تاریخچه', {
            'fields': ('code', 'level', 'path', 'created_at'),
            'classes': ('collapse',),
        }),
    )

    def ticket_count(self, obj):
        count = obj.ticket_set.count()
        return format_html(
            '<span style="background:#6366f1;color:white;padding:2px 8px;border-radius:12px;font-size:12px;">{} تیکت</span>',
            count
        )
    ticket_count.short_description = 'تعداد تیکت'


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('project', 'category', 'responsible_person', 'priority', 'is_active_badge', 'created_at')
    list_filter = ('is_active', 'project', 'category')
    search_fields = ('project__name', 'category__title', 'responsible_person__full_name')
    autocomplete_fields = ('project', 'category', 'responsible_person')
    readonly_fields = ('created_at',)

    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html(
                '<span style="background:#22c55e;color:white;padding:2px 8px;border-radius:12px;font-size:12px;">فعال</span>'
            )
        return format_html(
            '<span style="background:#94a3b8;color:white;padding:2px 8px;border-radius:12px;font-size:12px;">غیرفعال</span>'
        )
    is_active_badge.short_description = 'وضعیت'


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'status_badge', 'priority_badge', 'requester', 'assigned_to', 'deadline', 'created_at')
    search_fields = ('title', 'description')
    list_filter = (
        'status',
        'priority',
        'category',
        'project',
        ('deadline', JDateFieldListFilter),
    )
    autocomplete_fields = ('category', 'project', 'requester', 'assigned_to')
    readonly_fields = ('code', 'created_at', 'updated_at', 'resolved_at', 'closed_at')
    exclude = ('code',)
    fieldsets = (
        ('اطلاعات تیکت', {
            'fields': ('title', 'description'),
        }),
        ('دسته‌بندی و پروژه', {
            'fields': ('category', 'project'),
        }),
        ('تخصیص', {
            'fields': ('requester', 'assigned_to'),
        }),
        ('وضعیت و اولویت', {
            'fields': ('status', 'priority', 'deadline'),
        }),
        ('زمان‌ها', {
            'fields': ('code', 'resolved_at', 'closed_at', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def status_badge(self, obj):
        colors = {
            'open': '#f59e0b',
            'in_progress': '#3b82f6',
            'resolved': '#22c55e',
            'closed': '#94a3b8',
        }
        labels = {
            'open': 'باز',
            'in_progress': 'در حال انجام',
            'resolved': 'حل شده',
            'closed': 'بسته شده',
        }
        color = colors.get(obj.status, '#94a3b8')
        label = labels.get(obj.status, obj.status)
        return format_html(
            '<span style="background:{};color:white;padding:2px 8px;border-radius:12px;font-size:12px;">{}</span>',
            color, label
        )
    status_badge.short_description = 'وضعیت'

    def priority_badge(self, obj):
        colors = {
            'low': '#22c55e',
            'medium': '#f59e0b',
            'high': '#f97316',
            'critical': '#ef4444',
        }
        labels = {
            'low': 'کم',
            'medium': 'متوسط',
            'high': 'بالا',
            'critical': 'بحرانی',
        }
        color = colors.get(obj.priority, '#94a3b8')
        label = labels.get(obj.priority, obj.priority)
        return format_html(
            '<span style="background:{};color:white;padding:2px 8px;border-radius:12px;font-size:12px;">{}</span>',
            color, label
        )
    priority_badge.short_description = 'اولویت'


@admin.register(TicketMessage)
class TicketMessageAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'sender', 'message_type_badge', 'is_read_badge', 'created_at')
    search_fields = ('ticket__code', 'sender__full_name', 'message')
    list_filter = ('message_type', 'is_read')
    autocomplete_fields = ('ticket', 'sender')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('اطلاعات پیام', {
            'fields': ('ticket', 'sender', 'message_type', 'message'),
        }),
        ('فایل', {
            'fields': ('file_url', 'file_name'),
            'classes': ('collapse',),
        }),
        ('صوت', {
            'fields': ('audio_url', 'duration'),
            'classes': ('collapse',),
        }),
        ('وضعیت', {
            'fields': ('is_read', 'created_at'),
        }),
    )

    def message_type_badge(self, obj):
        colors = {'text': '#3b82f6', 'file': '#f59e0b', 'audio': '#22c55e'}
        labels = {'text': 'متن', 'file': 'فایل', 'audio': 'صوت'}
        color = colors.get(obj.message_type, '#94a3b8')
        label = labels.get(obj.message_type, obj.message_type)
        return format_html(
            '<span style="background:{};color:white;padding:2px 8px;border-radius:12px;font-size:12px;">{}</span>',
            color, label
        )
    message_type_badge.short_description = 'نوع'

    def is_read_badge(self, obj):
        if obj.is_read:
            return format_html(
                '<span style="background:#22c55e;color:white;padding:2px 8px;border-radius:12px;font-size:12px;">خوانده شده</span>'
            )
        return format_html(
            '<span style="background:#ef4444;color:white;padding:2px 8px;border-radius:12px;font-size:12px;">خوانده نشده</span>'
        )
    is_read_badge.short_description = 'وضعیت خواندن'
