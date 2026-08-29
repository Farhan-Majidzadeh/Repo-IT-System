from django.db import models
from django.core.validators import MinLengthValidator
from personnel.models import Personnel, Department
from django.utils.text import slugify
import uuid


class Warehouse(models.Model):
    code = models.CharField(max_length=20, unique=True, editable=False)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.code:
            base_code = slugify(self.name)[:8].upper() or 'WH'
            self.code = f"{base_code}-{uuid.uuid4().hex[:4].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = 'انبار'
        verbose_name_plural = 'انبارها'


class Asset(models.Model):
    ASSET_TYPES = (('fixed', 'دارایی ثابت'), ('consumable', 'مصرفی'))

    code = models.CharField(max_length=20, unique=True, editable=False)
    name = models.CharField(max_length=200)
    part_number = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    asset_type = models.CharField(max_length=20, choices=ASSET_TYPES, default='fixed')
    purchase_date = models.DateField(blank=True, null=True)
    invoice_number = models.CharField(max_length=50, blank=True, null=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    warranty_expiry = models.DateField(blank=True, null=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, null=True, blank=True)
    is_available = models.BooleanField(default=True)
    documents = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.code:
            base_code = slugify(self.name)[:8].upper() or 'AST'
            self.code = f"{base_code}-{uuid.uuid4().hex[:4].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = 'دارایی'
        verbose_name_plural = 'دارایی‌ها'


class AssetDelivery(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    delivery_date = models.DateField()
    return_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, default='active')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.asset} -> {self.personnel} در {self.delivery_date}"

    class Meta:
        verbose_name = 'تحویل دارایی'
        verbose_name_plural = 'تحویل دارایی‌ها'
