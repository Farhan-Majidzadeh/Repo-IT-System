from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from personnel.models import Personnel, Department, Branch
from django.utils.text import slugify
import uuid


class Supplier(models.Model):
    """تامین‌کنندگان و شرکت‌ها"""
    code = models.CharField(max_length=20, unique=True, editable=False)
    name = models.CharField(max_length=200, verbose_name='نام شرکت')
    contact_person = models.CharField(max_length=100, blank=True, null=True, verbose_name='فرد تماس')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='تلفن')
    email = models.EmailField(blank=True, null=True, verbose_name='ایمیل')
    address = models.TextField(blank=True, null=True, verbose_name='آدرس')
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.code:
            base_code = slugify(self.name)[:8].upper() or 'SUP'
            self.code = f"{base_code}-{uuid.uuid4().hex[:4].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'تأمین‌کننده'
        verbose_name_plural = 'تأمین‌کنندگان'


class Warehouse(models.Model):
    code = models.CharField(max_length=20, unique=True, editable=False)
    name = models.CharField(max_length=100)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='شعبه')
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


class AssetCategory(models.Model):
    """دسته‌بندی تجهیزات"""
    name = models.CharField(max_length=100, verbose_name='نام دسته')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    is_cartridge = models.BooleanField(default=False, verbose_name='کارتریج است')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'دسته تجهیزات'
        verbose_name_plural = 'دسته‌های تجهیزات'


class Asset(models.Model):
    ASSET_TYPES = (
        ('fixed', 'دارایی ثابت'),
        ('consumable', 'مصرفی'),
    )
    STATUS_CHOICES = (
        ('available', 'موجود'),
        ('in_use', 'در حال استفاده'),
        ('under_repair', 'در حال تعمیر'),
        ('under_charge', 'در حال شارژ'),
        ('scrapped', 'اوراق شده'),
    )

    code = models.CharField(max_length=20, unique=True, editable=False)
    name = models.CharField(max_length=200)
    asset_category = models.ForeignKey(AssetCategory, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='دسته تجهیزات')
    part_number = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    asset_type = models.CharField(max_length=20, choices=ASSET_TYPES, default='fixed')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')

    # اطلاعات خرید
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='تأمین‌کننده')
    purchase_date = models.DateField(blank=True, null=True, verbose_name='تاریخ خرید')
    invoice_number = models.CharField(max_length=50, blank=True, null=True, verbose_name='شماره فاکتور')
    price = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, verbose_name='قیمت')
    warranty_expiry = models.DateField(blank=True, null=True, verbose_name='انقضای گارانتی')
    purchase_documents = models.JSONField(default=dict, blank=True, verbose_name='مدارک خرید')

    # محل نگهداری
    warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, null=True, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='شعبه')
    is_available = models.BooleanField(default=True)
    documents = models.JSONField(default=dict, blank=True)

    # اطلاعات مصرفی‌ها
    usage_start_date = models.DateField(blank=True, null=True, verbose_name='تاریخ شروع مصرف')
    usage_end_date = models.DateField(blank=True, null=True, verbose_name='تاریخ پایان مصرف')

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


class AssetReferral(models.Model):
    """ارجاعات تجهیزات - تعمیر، شارژ، اوراق و..."""
    REFERRAL_TYPES = (
        ('repair', 'تعمیر'),
        ('charge', 'شارژ'),
        ('upgrade', 'ارتقا'),
        ('scrap', 'اوراق'),
        ('transfer', 'انتقال'),
        ('other', 'سایر'),
    )
    STATUS_CHOICES = (
        ('pending', 'در انتظار'),
        ('sent', 'ارسال شده'),
        ('in_progress', 'در حال انجام'),
        ('completed', 'انجام شده'),
        ('cancelled', 'لغو شده'),
    )

    code = models.CharField(max_length=20, unique=True, editable=False)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, verbose_name='تجهیز')
    referral_type = models.CharField(max_length=20, choices=REFERRAL_TYPES, verbose_name='نوع ارجاع')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='وضعیت')

    # ارجاع به
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='شرکت طرف قرارداد')
    destination = models.CharField(max_length=200, blank=True, null=True, verbose_name='محل ارسال')
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات')

    # تاریخ‌ها
    send_date = models.DateField(blank=True, null=True, verbose_name='تاریخ ارسال')
    return_date = models.DateField(blank=True, null=True, verbose_name='تاریخ بازگشت')

    # هزینه
    cost = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, verbose_name='هزینه')

    # امتیازدهی
    quality_rating = models.PositiveIntegerField(
        blank=True, null=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='امتیاز کیفیت'
    )
    rating_comment = models.TextField(blank=True, null=True, verbose_name='نظر درباره کیفیت')

    # فرستنده
    sent_by = models.ForeignKey(Personnel, on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_referrals', verbose_name='ارسال‌کننده')
    received_by = models.ForeignKey(Personnel, on_delete=models.SET_NULL, null=True, blank=True, related_name='received_referrals', verbose_name='دریافت‌کننده')

    # مدارک
    documents = models.JSONField(default=dict, blank=True, verbose_name='مدارک پیوست')

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.code:
            type_codes = {'repair': 'RPR', 'charge': 'CHR', 'upgrade': 'UPG', 'scrap': 'SCR', 'transfer': 'TRF', 'other': 'OTH'}
            base_code = type_codes.get(self.referral_type, 'REF')
            self.code = f"{base_code}-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.code} - {self.asset} ({self.get_referral_type_display()})"

    class Meta:
        verbose_name = 'ارجاع تجهیزات'
        verbose_name_plural = 'ارجاعات تجهیزات'


class CartridgeCharge(models.Model):
    """شارژ کارتریج"""
    STATUS_CHOICES = (
        ('sent', 'ارسال شده'),
        ('charging', 'در حال شارژ'),
        ('returned', 'برگشت داده شده'),
        ('cancelled', 'لغو شده'),
    )

    code = models.CharField(max_length=20, unique=True, editable=False)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, verbose_name='کارتریج')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name='شرکت شارژ')

    # تاریخ‌ها
    send_date = models.DateField(verbose_name='تاریخ ارسال')
    return_date = models.DateField(blank=True, null=True, verbose_name='تاریخ بازگشت')

    # وضعیت
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='sent', verbose_name='وضعیت')

    # اطلاعات
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='هزینه شارژ')
    page_count = models.PositiveIntegerField(blank=True, null=True, verbose_name='تعداد صفحات چاپ شده پس از شارژ')

    # امتیازدهی
    quality_rating = models.PositiveIntegerField(
        blank=True, null=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='امتیاز کیفیت'
    )
    speed_rating = models.PositiveIntegerField(
        blank=True, null=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='امتیاز سرعت'
    )
    rating_comment = models.TextField(blank=True, null=True, verbose_name='نظر درباره کیفیت')

    # افراد
    sent_by = models.ForeignKey(Personnel, on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_charges', verbose_name='ارسال‌کننده')
    received_by = models.ForeignKey(Personnel, on_delete=models.SET_NULL, null=True, blank=True, related_name='received_charges', verbose_name='دریافت‌کننده')
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='شعبه')

    notes = models.TextField(blank=True, null=True, verbose_name='توضیحات')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = f"CHR-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.code} - {self.asset} - {self.supplier}"

    class Meta:
        verbose_name = 'شارژ کارتریج'
        verbose_name_plural = 'شارژهای کارتریج'


class AssetDelivery(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='شعبه')
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
