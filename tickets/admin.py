from django.contrib import admin
from django import forms
from django.utils.html import format_html
from django_jalali.admin.filters import JDateFieldListFilter
import django_jalali.admin as jadmin
from .models import TicketCategory, Assignment, Ticket, TicketMessage
from personnel.models import Personnel


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
    list_display = ('project', 'category', 'responsible_person', 'branch_name', 'priority', 'is_active_badge', 'created_at')
    list_filter = ('is_active', 'project', 'category', 'branch')
    search_fields = ('project__name', 'category__title', 'responsible_person__full_name')
    readonly_fields = ('created_at',)
    autocomplete_fields = ('project', 'category', 'responsible_person', 'branch')

    def branch_name(self, obj):
        if obj.branch:
            return obj.branch.name
        return '-'
    branch_name.short_description = 'شعبه'

    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="background:#22c55e;color:white;padding:2px 8px;border-radius:12px;font-size:12px;">فعال</span>')
        return format_html('<span style="background:#94a3b8;color:white;padding:2px 8px;border-radius:12px;font-size:12px;">غیرفعال</span>')
    is_active_badge.short_description = 'وضعیت'


class TicketAdminForm(forms.ModelForm):
    """فرم سفارشی تیکت با فیلتر شعبه"""
    class Meta:
        model = Ticket
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'target_branch' in self.fields:
            self.fields['target_branch'].label = 'ارجاع به واحد IT'
        if 'branch' in self.fields:
            self.fields['branch'].label = 'شعبه'


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    form = TicketAdminForm
    list_display = ('code', 'title', 'status_badge', 'priority_badge', 'branch_name', 'target_branch_name', 'requester', 'assigned_to', 'response_time', 'created_at')
    search_fields = ('title', 'description', 'requester__full_name', 'assigned_to__full_name')
    list_filter = (
        'status',
        'priority',
        'category',
        'project',
        'branch',
        'target_branch',
        ('deadline', JDateFieldListFilter),
        ('created_at', JDateFieldListFilter),
    )
    readonly_fields = ('code', 'created_at', 'updated_at', 'resolved_at', 'closed_at')
    exclude = ('code',)
    autocomplete_fields = ('category', 'project', 'requester', 'assigned_to', 'branch', 'target_branch')
    fieldsets = (
        ('اطلاعات تیکت', {
            'fields': ('title', 'description'),
        }),
        ('شعبه و ارجاع', {
            'fields': ('branch', 'target_branch'),
            'description': 'شعبه مبدا و واحد IT مقصد',
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

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # کارشناس IT فقط تیکت‌های شعبه خودش رو ببینه
        try:
            personnel = request.user.personnel_profile
            if personnel.is_it_specialist:
                return qs.filter(target_branch=personnel.branch)
        except:
            pass
        return qs

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """فیلتر کارشناسان IT بر اساس شعبه انتخاب شده"""
        if db_field.name == 'assigned_to':
            # اگه شعبه مقصد مشخص باشه، فقط کارشناسان IT اون شعبه
            if request.POST.get('target_branch'):
                kwargs['queryset'] = Personnel.objects.filter(
                    is_it_specialist=True,
                    branch_id=request.POST.get('target_branch'),
                    is_active=True
                )
            else:
                kwargs['queryset'] = Personnel.objects.filter(
                    is_it_specialist=True,
                    is_active=True
                )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def branch_name(self, obj):
        if obj.branch:
            return obj.branch.name
        return '-'
    branch_name.short_description = 'شعبه'

    def target_branch_name(self, obj):
        if obj.target_branch:
            return format_html('<span style="background:#3b82f6;color:white;padding:2px 8px;border-radius:12px;font-size:12px;">{}</span>', obj.target_branch.name)
        return '-'
    target_branch_name.short_description = ' واحد IT مقصد'

    def response_time(self, obj):
        if obj.resolved_at and obj.created_at:
            diff = obj.resolved_at - obj.created_at
            hours = diff.total_seconds() / 3600
            if hours < 1:
                return format_html('<span style="color:#22c55e;">{} دقیقه</span>', int(diff.total_seconds() / 60))
            elif hours < 24:
                return format_html('<span style="color:#f59e0b;">{} ساعت</span>', int(hours))
            else:
                return format_html('<span style="color:#ef4444;">{} روز</span>', int(hours / 24))
        return '-'
    response_time.short_description = 'زمان پاسخ'

    def status_badge(self, obj):
        colors = {'open': '#f59e0b', 'in_progress': '#3b82f6', 'resolved': '#22c55e', 'closed': '#94a3b8'}
        labels = {'open': 'باز', 'in_progress': 'در حال انجام', 'resolved': 'حل شده', 'closed': 'بسته شده'}
        color = colors.get(obj.status, '#94a3b8')
        label = labels.get(obj.status, obj.status)
        return format_html('<span style="background:{};color:white;padding:2px 8px;border-radius:12px;font-size:12px;">{}</span>', color, label)
    status_badge.short_description = 'وضعیت'

    def priority_badge(self, obj):
        colors = {'low': '#22c55e', 'medium': '#f59e0b', 'high': '#f97316', 'critical': '#ef4444'}
        labels = {'low': 'کم', 'medium': 'متوسط', 'high': 'بالا', 'critical': 'بحرانی'}
        color = colors.get(obj.priority, '#94a3b8')
        label = labels.get(obj.priority, obj.priority)
        return format_html('<span style="background:{};color:white;padding:2px 8px;border-radius:12px;font-size:12px;">{}</span>', color, label)
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
        return format_html('<span style="background:{};color:white;padding:2px 8px;border-radius:12px;font-size:12px;">{}</span>', color, label)
    message_type_badge.short_description = 'نوع'

    def is_read_badge(self, obj):
        if obj.is_read:
            return format_html('<span style="background:#22c55e;color:white;padding:2px 8px;border-radius:12px;font-size:12px;">خوانده شده</span>')
        return format_html('<span style="background:#ef4444;color:white;padding:2px 8px;border-radius:12px;font-size:12px;">خوانده نشده</span>')
    is_read_badge.short_description = 'وضعیت خواندن'
