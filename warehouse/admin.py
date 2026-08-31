from django.contrib import admin
from django.utils.html import format_html
from django_jalali.admin.filters import JDateFieldListFilter
import django_jalali.admin as jadmin
from .models import Supplier, Warehouse, AssetCategory, Asset, AssetReferral, CartridgeCharge, AssetDelivery


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'contact_person', 'phone', 'email', 'is_active_badge', 'created_at')
    search_fields = ('name', 'contact_person', 'phone', 'email')
    list_filter = ('is_active',)
    readonly_fields = ('code', 'created_at')
    exclude = ('code',)
    fieldsets = (
        ('اطلاعات شرکت', {
            'fields': ('name', 'contact_person', 'phone', 'email', 'address'),
        }),
        ('توضیحات', {
            'fields': ('description',),
        }),
        ('وضعیت', {
            'fields': ('is_active',),
        }),
        ('تاریخچه', {
            'fields': ('code', 'created_at'),
            'classes': ('collapse',),
        }),
    )

    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="background:#22c55e;color:white;padding:2px 8px;border-radius:12px;font-size:12px;">فعال</span>')
        return format_html('<span style="background:#ef4444;color:white;padding:2px 8px;border-radius:12px;font-size:12px;">غیرفعال</span>')
    is_active_badge.short_description = 'وضعیت'


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'branch_name', 'location', 'asset_count', 'created_at')
    search_fields = ('name', 'location')
    list_filter = ('branch',)
    readonly_fields = ('code', 'created_at')
    exclude = ('code',)
    autocomplete_fields = ('branch',)
    fieldsets = (
        ('اطلاعات انبار', {
            'fields': ('name', 'branch', 'location', 'description'),
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

    def asset_count(self, obj):
        count = obj.asset_set.count()
        return format_html(
            '<span style="background:#6366f1;color:white;padding:2px 8px;border-radius:12px;font-size:12px;">{} دارایی</span>',
            count
        )
    asset_count.short_description = 'تعداد دارایی'


@admin.register(AssetCategory)
class AssetCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'is_cartridge_badge', 'asset_count')
    search_fields = ('name',)
    list_filter = ('is_cartridge',)
    list_editable = ('is_cartridge',)

    def is_cartridge_badge(self, obj):
        if obj.is_cartridge:
            return format_html('<span style="background:#f59e0b;color:white;padding:2px 8px;border-radius:12px;font-size:12px;">کارتریج</span>')
        return '-'
    is_cartridge_badge.short_description = 'نوع'

    def asset_count(self, obj):
        count = obj.asset_set.count()
        return format_html('<span style="background:#6366f1;color:white;padding:2px 8px;border-radius:12px;font-size:12px;">{}</span>', count)
    asset_count.short_description = 'تعداد'


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'asset_type_badge', 'status_badge', 'asset_category', 'branch_name', 'supplier', 'price_formatted', 'is_available_badge')
    search_fields = ('name', 'part_number')
    list_filter = (
        'asset_type',
        'status',
        'is_available',
        'warehouse',
        'branch',
        'asset_category',
        'supplier',
        ('purchase_date', JDateFieldListFilter),
    )
    readonly_fields = ('code', 'created_at')
    exclude = ('code',)
    autocomplete_fields = ('supplier', 'warehouse', 'branch', 'asset_category')
    fieldsets = (
        ('اطلاعات دارایی', {
            'fields': ('name', 'part_number', 'asset_category', 'asset_type', 'status'),
        }),
        ('تأمین‌کننده و خرید', {
            'fields': ('supplier', 'purchase_date', 'invoice_number', 'price', 'warranty_expiry'),
        }),
        ('محل نگهداری', {
            'fields': ('warehouse', 'branch', 'is_available'),
        }),
        ('اطلاعات مصرفی', {
            'fields': ('usage_start_date', 'usage_end_date'),
            'description': 'فقط برای کالاهای مصرفی',
            'classes': ('collapse',),
        }),
        ('مستندات', {
            'fields': ('documents', 'purchase_documents'),
            'classes': ('collapse',),
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

    def asset_type_badge(self, obj):
        colors = {'fixed': '#6366f1', 'consumable': '#f59e0b'}
        labels = {'fixed': 'ثابت', 'consumable': 'مصرفی'}
        color = colors.get(obj.asset_type, '#94a3b8')
        label = labels.get(obj.asset_type, obj.asset_type)
        return format_html('<span style="background:{};color:white;padding:2px 8px;border-radius:12px;font-size:12px;">{}</span>', color, label)
    asset_type_badge.short_description = 'نوع'

    def status_badge(self, obj):
        colors = {'available': '#22c55e', 'in_use': '#3b82f6', 'under_repair': '#f59e0b', 'under_charge': '#f97316', 'scrapped': '#ef4444'}
        labels = {'available': 'موجود', 'in_use': 'در حال استفاده', 'under_repair': 'در حال تعمیر', 'under_charge': 'شارژ', 'scrapped': 'اوراق'}
        color = colors.get(obj.status, '#94a3b8')
        label = labels.get(obj.status, obj.status)
        return format_html('<span style="background:{};color:white;padding:2px 8px;border-radius:12px;font-size:12px;">{}</span>', color, label)
    status_badge.short_description = 'وضعیت'

    def price_formatted(self, obj):
        if obj.price:
            return format_html('{:,.0f} تومان', obj.price)
        return '-'
    price_formatted.short_description = 'قیمت'

    def is_available_badge(self, obj):
        if obj.is_available:
            return format_html('<span style="background:#22c55e;color:white;padding:2px 8px;border-radius:12px;font-size:12px;">موجود</span>')
        return format_html('<span style="background:#ef4444;color:white;padding:2px 8px;border-radius:12px;font-size:12px;">تحویل شده</span>')
    is_available_badge.short_description = 'وضعیت'


@admin.register(AssetReferral)
class AssetReferralAdmin(admin.ModelAdmin):
    list_display = ('code', 'asset', 'referral_type_badge', 'status_badge', 'supplier', 'send_date', 'return_date', 'cost_formatted', 'quality_stars')
    search_fields = ('asset__name', 'asset__code', 'supplier__name', 'description')
    list_filter = (
        'referral_type',
        'status',
        'supplier',
        ('send_date', JDateFieldListFilter),
        ('return_date', JDateFieldListFilter),
    )
    readonly_fields = ('code', 'created_at')
    exclude = ('code',)
    autocomplete_fields = ('asset', 'supplier', 'sent_by', 'received_by')
    fieldsets = (
        ('اطلاعات ارجاع', {
            'fields': ('asset', 'referral_type', 'status'),
        }),
        ('مقصد', {
            'fields': ('supplier', 'destination', 'description'),
        }),
        ('تاریخ‌ها', {
            'fields': ('send_date', 'return_date'),
        }),
        ('هزینه و امتیاز', {
            'fields': ('cost', 'quality_rating', 'rating_comment'),
        }),
        ('افراد', {
            'fields': ('sent_by', 'received_by'),
        }),
        ('مدارک', {
            'fields': ('documents',),
            'classes': ('collapse',),
        }),
        ('تاریخچه', {
            'fields': ('code', 'created_at'),
            'classes': ('collapse',),
        }),
    )

    def referral_type_badge(self, obj):
        colors = {'repair': '#ef4444', 'charge': '#f59e0b', 'upgrade': '#3b82f6', 'scrap': '#94a3b8', 'transfer': '#22c55e', 'other': '#6366f1'}
        color = colors.get(obj.referral_type, '#94a3b8')
        label = obj.get_referral_type_display()
        return format_html('<span style="background:{};color:white;padding:2px 8px;border-radius:12px;font-size:12px;">{}</span>', color, label)
    referral_type_badge.short_description = 'نوع'

    def status_badge(self, obj):
        colors = {'pending': '#f59e0b', 'sent': '#3b82f6', 'in_progress': '#f97316', 'completed': '#22c55e', 'cancelled': '#ef4444'}
        labels = {'pending': 'در انتظار', 'sent': 'ارسال شده', 'in_progress': 'در حال انجام', 'completed': 'انجام شده', 'cancelled': 'لغو شده'}
        color = colors.get(obj.status, '#94a3b8')
        label = labels.get(obj.status, obj.status)
        return format_html('<span style="background:{};color:white;padding:2px 8px;border-radius:12px;font-size:12px;">{}</span>', color, label)
    status_badge.short_description = 'وضعیت'

    def cost_formatted(self, obj):
        if obj.cost:
            return format_html('{:,.0f} تومان', obj.cost)
        return '-'
    cost_formatted.short_description = 'هزینه'

    def quality_stars(self, obj):
        if obj.quality_rating:
            stars = '★' * obj.quality_rating + '☆' * (5 - obj.quality_rating)
            return format_html('<span style="color:#f59e0b;font-size:14px;">{}</span>', stars)
        return '-'
    quality_stars.short_description = 'امتیاز'


@admin.register(CartridgeCharge)
class CartridgeChargeAdmin(admin.ModelAdmin):
    list_display = ('code', 'asset', 'supplier', 'branch_name', 'send_date', 'return_date', 'status_badge', 'cost_formatted', 'quality_stars', 'speed_stars')
    search_fields = ('asset__name', 'asset__code', 'supplier__name')
    list_filter = (
        'status',
        'supplier',
        'branch',
        ('send_date', JDateFieldListFilter),
        ('return_date', JDateFieldListFilter),
    )
    readonly_fields = ('code', 'created_at')
    exclude = ('code',)
    autocomplete_fields = ('asset', 'supplier', 'sent_by', 'received_by', 'branch')
    fieldsets = (
        ('اطلاعات شارژ', {
            'fields': ('asset', 'supplier', 'status', 'branch'),
        }),
        ('تاریخ‌ها', {
            'fields': ('send_date', 'return_date'),
        }),
        ('هزینه و کیفیت', {
            'fields': ('cost', 'page_count', 'quality_rating', 'speed_rating', 'rating_comment'),
        }),
        ('افراد', {
            'fields': ('sent_by', 'received_by'),
        }),
        ('توضیحات', {
            'fields': ('notes',),
            'classes': ('collapse',),
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

    def status_badge(self, obj):
        colors = {'sent': '#3b82f6', 'charging': '#f59e0b', 'returned': '#22c55e', 'cancelled': '#ef4444'}
        labels = {'sent': 'ارسال شده', 'charging': 'در حال شارژ', 'returned': 'برگشت', 'cancelled': 'لغو'}
        color = colors.get(obj.status, '#94a3b8')
        label = labels.get(obj.status, obj.status)
        return format_html('<span style="background:{};color:white;padding:2px 8px;border-radius:12px;font-size:12px;">{}</span>', color, label)
    status_badge.short_description = 'وضعیت'

    def cost_formatted(self, obj):
        if obj.cost:
            return format_html('{:,.0f} تومان', obj.cost)
        return '-'
    cost_formatted.short_description = 'هزینه'

    def quality_stars(self, obj):
        if obj.quality_rating:
            stars = '★' * obj.quality_rating + '☆' * (5 - obj.quality_rating)
            return format_html('<span style="color:#f59e0b;font-size:14px;">{}</span>', stars)
        return '-'
    quality_stars.short_description = 'کیفیت'

    def speed_stars(self, obj):
        if obj.speed_rating:
            stars = '★' * obj.speed_rating + '☆' * (5 - obj.speed_rating)
            return format_html('<span style="color:#3b82f6;font-size:14px;">{}</span>', stars)
        return '-'
    speed_stars.short_description = 'سرعت'


@admin.register(AssetDelivery)
class AssetDeliveryAdmin(admin.ModelAdmin):
    list_display = ('asset', 'personnel', 'department', 'branch_name', 'delivery_date', 'return_date', 'status_badge')
    search_fields = ('asset__name', 'personnel__full_name')
    list_filter = ('status', 'department', 'branch')
    autocomplete_fields = ('asset', 'personnel', 'department', 'branch')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('اطلاعات تحویل', {
            'fields': ('asset', 'personnel', 'department', 'branch'),
        }),
        ('تاریخ‌ها و وضعیت', {
            'fields': ('delivery_date', 'return_date', 'status'),
        }),
        ('توضیحات', {
            'fields': ('notes',),
            'classes': ('collapse',),
        }),
    )

    def branch_name(self, obj):
        if obj.branch:
            return obj.branch.name
        return '-'
    branch_name.short_description = 'شعبه'

    def status_badge(self, obj):
        colors = {'active': '#22c55e', 'returned': '#94a3b8', 'overdue': '#ef4444'}
        labels = {'active': 'فعال', 'returned': 'برگشت داده شده', 'overdue': 'سررسید شده'}
        color = colors.get(obj.status, '#94a3b8')
        label = labels.get(obj.status, obj.status)
        return format_html('<span style="background:{};color:white;padding:2px 8px;border-radius:12px;font-size:12px;">{}</span>', color, label)
    status_badge.short_description = 'وضعیت'
