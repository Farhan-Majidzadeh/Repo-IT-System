from django.contrib import admin
from django.utils.html import format_html
from .models import Warehouse, Asset, AssetDelivery


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'location', 'asset_count', 'created_at')
    search_fields = ('name', 'location')
    readonly_fields = ('code', 'created_at')
    exclude = ('code',)
    fieldsets = (
        ('اطلاعات انبار', {
            'fields': ('name', 'location', 'description'),
        }),
        ('تاریخچه', {
            'fields': ('code', 'created_at'),
            'classes': ('collapse',),
        }),
    )

    def asset_count(self, obj):
        count = obj.asset_set.count()
        return format_html(
            '<span style="background:#6366f1;color:white;padding:2px 8px;border-radius:12px;font-size:12px;">{} دارایی</span>',
            count
        )
    asset_count.short_description = 'تعداد دارایی'

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'asset_type_badge', 'category', 'warehouse', 'price_formatted', 'is_available_badge')
    search_fields = ('name', 'part_number')
    list_filter = ('asset_type', 'is_available', 'warehouse', 'category')
    readonly_fields = ('code', 'created_at')
    exclude = ('code',)
    fieldsets = (
        ('اطلاعات دارایی', {
            'fields': ('name', 'part_number', 'category', 'asset_type'),
        }),
        ('اطلاعات مالی', {
            'fields': ('purchase_date', 'invoice_number', 'price', 'warranty_expiry'),
        }),
        ('محل نگهداری', {
            'fields': ('warehouse', 'is_available'),
        }),
        ('مستندات', {
            'fields': ('documents',),
            'classes': ('collapse',),
        }),
        ('تاریخچه', {
            'fields': ('code', 'created_at'),
            'classes': ('collapse',),
        }),
    )

    def asset_type_badge(self, obj):
        colors = {'fixed': '#6366f1', 'consumable': '#f59e0b'}
        labels = {'fixed': 'ثابت', 'consumable': 'مصرفی'}
        color = colors.get(obj.asset_type, '#94a3b8')
        label = labels.get(obj.asset_type, obj.asset_type)
        return format_html(
            '<span style="background:{};color:white;padding:2px 8px;border-radius:12px;font-size:12px;">{}</span>',
            color, label
        )
    asset_type_badge.short_description = 'نوع'

    def price_formatted(self, obj):
        if obj.price:
            return format_html('{:,.0f} تومان', obj.price)
        return '-'
    price_formatted.short_description = 'قیمت'

    def is_available_badge(self, obj):
        if obj.is_available:
            return format_html(
                '<span style="background:#22c55e;color:white;padding:2px 8px;border-radius:12px;font-size:12px;">موجود</span>'
            )
        return format_html(
            '<span style="background:#ef4444;color:white;padding:2px 8px;border-radius:12px;font-size:12px;">تحویل شده</span>'
        )
    is_available_badge.short_description = 'وضعیت'

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }


@admin.register(AssetDelivery)
class AssetDeliveryAdmin(admin.ModelAdmin):
    list_display = ('asset', 'personnel', 'department', 'delivery_date', 'return_date', 'status_badge')
    search_fields = ('asset__name', 'personnel__full_name')
    list_filter = ('status', 'department')
    raw_id_fields = ('asset', 'personnel', 'department')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('اطلاعات تحویل', {
            'fields': ('asset', 'personnel', 'department'),
        }),
        ('تاریخ‌ها و وضعیت', {
            'fields': ('delivery_date', 'return_date', 'status'),
        }),
        ('توضیحات', {
            'fields': ('notes',),
            'classes': ('collapse',),
        }),
    )

    def status_badge(self, obj):
        colors = {
            'active': '#22c55e',
            'returned': '#94a3b8',
            'overdue': '#ef4444',
        }
        labels = {
            'active': 'فعال',
            'returned': 'برگشت داده شده',
            'overdue': 'سررسید شده',
        }
        color = colors.get(obj.status, '#94a3b8')
        label = labels.get(obj.status, obj.status)
        return format_html(
            '<span style="background:{};color:white;padding:2px 8px;border-radius:12px;font-size:12px;">{}</span>',
            color, label
        )
    status_badge.short_description = 'وضعیت'

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
