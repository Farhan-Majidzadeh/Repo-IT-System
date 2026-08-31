from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django import forms
from django_jalali.admin.filters import JDateFieldListFilter
import django_jalali.admin as jadmin
from .models import Branch, Department, Personnel, PersonnelDepartment


class PersonnelCreateUserForm(forms.ModelForm):
    create_user = forms.BooleanField(
        label='ایجاد حساب کاربری',
        required=False,
        initial=True,
        help_text='اگر تیک بزنید، یک حساب کاربری جنگو برای این پرسنل ساخته می‌شود'
    )

    class Meta:
        model = Personnel
        fields = '__all__'


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'city', 'phone', 'manager', 'personnel_count', 'is_active_badge', 'created_at')
    search_fields = ('name', 'city', 'address')
    list_filter = ('city', 'is_active')
    readonly_fields = ('code', 'created_at')
    exclude = ('code',)
    fieldsets = (
        ('اطلاعات شعبه', {
            'fields': ('name', 'city', 'address', 'phone', 'manager'),
        }),
        ('وضعیت', {
            'fields': ('is_active',),
        }),
        ('تاریخچه', {
            'fields': ('code', 'created_at'),
            'classes': ('collapse',),
        }),
    )

    def personnel_count(self, obj):
        count = obj.personnel_set.count()
        return format_html(
            '<span style="background:#6366f1;color:white;padding:2px 8px;border-radius:12px;font-size:12px;">{} نفر</span>',
            count
        )
    personnel_count.short_description = 'تعداد پرسنل'

    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="background:#22c55e;color:white;padding:2px 8px;border-radius:12px;font-size:12px;">فعال</span>')
        return format_html('<span style="background:#ef4444;color:white;padding:2px 8px;border-radius:12px;font-size:12px;">غیرفعال</span>')
    is_active_badge.short_description = 'وضعیت'


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'branch_name', 'building', 'personnel_count', 'created_at')
    search_fields = ('name', 'building')
    list_filter = ('branch', 'building')
    readonly_fields = ('code', 'created_at')
    exclude = ('code',)
    autocomplete_fields = ('branch',)
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('name', 'branch', 'building'),
        }),
        ('تاریخچه', {
            'fields': ('code', 'created_at'),
            'classes': ('collapse',),
        }),
    )

    def branch_name(self, obj):
        if obj.branch:
            return obj.branch.name
        return '-'
    branch_name.short_description = 'شعبه'

    def personnel_count(self, obj):
        count = obj.personneldepartment_set.count()
        return format_html(
            '<span style="background:#6366f1;color:white;padding:2px 8px;border-radius:12px;font-size:12px;">{}</span>',
            count
        )
    personnel_count.short_description = 'تعداد پرسنل'


@admin.register(Personnel)
class PersonnelAdmin(admin.ModelAdmin):
    form = PersonnelCreateUserForm
    list_display = ('personnel_code', 'full_name', 'branch_name', 'email', 'phone', 'it_badge', 'user_badge', 'is_active_badge', 'created_at')
    search_fields = ('full_name', 'email', 'phone', 'personnel_code')
    list_filter = (
        'is_active',
        'is_it_specialist',
        'branch',
        ('entry_date', JDateFieldListFilter),
    )
    readonly_fields = ('personnel_code', 'created_at')
    exclude = ('personnel_code',)
    autocomplete_fields = ('branch',)
    fieldsets = (
        ('اطلاعات شخصی', {
            'fields': ('full_name', 'email', 'phone'),
        }),
        ('اطلاعات استخدام', {
            'fields': ('branch', 'entry_date', 'settlement_date', 'is_active', 'is_it_specialist'),
        }),
        ('حساب کاربری', {
            'fields': ('user', 'create_user'),
            'description': 'حساب کاربری جنگو برای دسترسی به سیستم',
        }),
        ('تاریخچه', {
            'fields': ('personnel_code', 'created_at'),
            'classes': ('collapse',),
        }),
    )

    def save_model(self, request, obj, form, change):
        if form.cleaned_data.get('create_user') and not obj.user:
            username = obj.email.split('@')[0] if obj.email else obj.personnel_code.lower()
            password = f"ChangeMe123!"
            user = User.objects.create_user(
                username=username,
                email=obj.email or '',
                password=password,
                first_name=obj.full_name.split(' ')[0] if obj.full_name else '',
                last_name=' '.join(obj.full_name.split(' ')[1:]) if obj.full_name and len(obj.full_name.split(' ')) > 1 else '',
                is_active=obj.is_active,
            )
            obj.user = user
        super().save_model(request, obj, form, change)

    def branch_name(self, obj):
        if obj.branch:
            return obj.branch.name
        return '-'
    branch_name.short_description = 'شعبه'

    def it_badge(self, obj):
        if obj.is_it_specialist:
            return format_html('<span style="background:#3b82f6;color:white;padding:2px 8px;border-radius:12px;font-size:12px;">IT</span>')
        return '-'
    it_badge.short_description = 'کارشناس IT'

    def user_badge(self, obj):
        if obj.user:
            return format_html('<span style="background:#22c55e;color:white;padding:2px 8px;border-radius:12px;font-size:12px;">✓ دارد</span>')
        return format_html('<span style="background:#ef4444;color:white;padding:2px 8px;border-radius:12px;font-size:12px;">✗ ندارد</span>')
    user_badge.short_description = 'حساب کاربری'

    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="background:#22c55e;color:white;padding:2px 8px;border-radius:12px;font-size:12px;">فعال</span>')
        return format_html('<span style="background:#ef4444;color:white;padding:2px 8px;border-radius:12px;font-size:12px;">غیرفعال</span>')
    is_active_badge.short_description = 'وضعیت'


class PersonnelInline(admin.StackedInline):
    model = Personnel
    can_delete = False
    verbose_name_plural = 'اطلاعات پرسنل'
    fields = ('personnel_code', 'full_name', 'phone', 'branch', 'entry_date', 'is_active')
    readonly_fields = ('personnel_code',)


class UserAdmin(BaseUserAdmin):
    inlines = (PersonnelInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'personnel_badge', 'is_staff', 'is_active')

    def personnel_badge(self, obj):
        try:
            personnel = obj.personnel_profile
            return format_html(
                '<span style="background:#6366f1;color:white;padding:2px 8px;border-radius:12px;font-size:12px;">{}</span>',
                personnel.full_name
            )
        except Personnel.DoesNotExist:
            return format_html('<span style="color:#94a3b8;font-size:12px;">ندارد</span>')
    personnel_badge.short_description = 'پرسنل'


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(PersonnelDepartment)
class PersonnelDepartmentAdmin(admin.ModelAdmin):
    list_display = ('personnel', 'department', 'branch_name', 'entry_date', 'exit_date', 'is_current_badge')
    list_filter = ('is_current', 'department', 'branch')
    search_fields = ('personnel__full_name', 'department__name')
    autocomplete_fields = ('personnel', 'department', 'branch')

    def branch_name(self, obj):
        if obj.branch:
            return obj.branch.name
        return '-'
    branch_name.short_description = 'شعبه'

    def is_current_badge(self, obj):
        if obj.is_current:
            return format_html('<span style="background:#22c55e;color:white;padding:2px 8px;border-radius:12px;font-size:12px;">فعلی</span>')
        return format_html('<span style="background:#94a3b8;color:white;padding:2px 8px;border-radius:12px;font-size:12px;"> سابق</span>')
    is_current_badge.short_description = 'وضعیت'
