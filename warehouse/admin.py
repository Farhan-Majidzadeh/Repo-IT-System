from django.contrib import admin
from .models import Warehouse, Asset, AssetDelivery

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'location')

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'asset_type', 'warehouse', 'is_available')
    search_fields = ('code', 'name', 'part_number')

@admin.register(AssetDelivery)
class AssetDeliveryAdmin(admin.ModelAdmin):
    list_display = ('asset', 'personnel', 'delivery_date', 'status')
