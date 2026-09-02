import hashlib
import secrets
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.signing import Signer, BadSignature


signer = Signer()


def encrypt_value(value):
    """رمزنگاری مقدار"""
    if not value:
        return ''
    return signer.sign(value)


def decrypt_value(encrypted_value):
    """رمزگشایی مقدار"""
    if not encrypted_value:
        return ''
    try:
        return signer.unsign(encrypted_value)
    except BadSignature:
        return encrypted_value


class CredentialCategory(models.Model):
    """دسته‌بندی اطلاعات دسترسی"""

    TYPE_CHOICES = [
        ('domain', 'دامین / Active Directory'),
        ('mail', 'سرویس ایمیل'),
        ('server', 'سرور'),
        ('network', 'تجهیزات شبکه'),
        ('printer', 'چاپگر'),
        ('website', 'وب‌سایت / پنل'),
        ('database', 'پایگاه داده'),
        ('vpn', 'VPN'),
        ('backup', 'پشتیبان‌گیری'),
        ('cloud', 'سرویس ابری'),
        ('software', 'نرم‌افزار'),
        ('camera', 'دوربین مداربسته'),
        ('ups', 'UPS / برق اضطراری'),
        ('other', 'سایر'),
    ]

    name = models.CharField(_('نام دسته‌بندی'), max_length=100)
    category_type = models.CharField(_('نوع'), max_length=20, choices=TYPE_CHOICES, default='other')
    icon = models.CharField(_('آیکون Material'), max_length=50, default='vpn_key', help_text='نام آیکون Material Icons')
    description = models.TextField(_('توضیحات'), blank=True, null=True)
    is_active = models.BooleanField(_('فعال'), default=True)
    order = models.IntegerField(_('ترتیب'), default=0)

    class Meta:
        verbose_name = _('دسته‌بندی دسترسی')
        verbose_name_plural = _('دسته‌بندی‌های دسترسی')
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.get_category_type_display()} - {self.name}"


class Credential(models.Model):
    """اطلاعات دسترسی / لاگین"""

    SECURITY_LEVEL_CHOICES = [
        ('low', '🟢 عادی'),
        ('medium', '🟡 متوسط'),
        ('high', '🟠 حساس'),
        ('critical', '🔴 بحرانی'),
    ]

    STATUS_CHOICES = [
        ('active', 'فعال'),
        ('inactive', 'غیرفعال'),
        ('expired', 'منقضی شده'),
        ('archived', 'بایگانی شده'),
    ]

    # اطلاعات اصلی
    title = models.CharField(_('عنوان'), max_length=200, help_text='مثال: لاگین دامین مشهد')
    category = models.ForeignKey(CredentialCategory, on_delete=models.PROTECT, verbose_name=_('دسته‌بندی'), related_name='credentials')
    branch = models.ForeignKey('personnel.Branch', on_delete=models.SET_NULL, verbose_name=_('شعبه'), null=True, blank=True, related_name='credentials')

    # اطلاعات اتصال
    hostname = models.CharField(_('Hostname / IP'), max_length=255, blank=True, null=True, help_text='آدرس IP یا hostname سرور/دستگاه')
    port = models.CharField(_('پورت'), max_length=10, blank=True, null=True, help_text='پورت اتصال (مثال: 3389, 443)')
    url = models.URLField(_('آدرس URL'), blank=True, null=True, help_text='آدرس وب‌سایت یا پنل')

    # اطلاعات کاربری
    username = models.CharField(_('نام کاربری'), max_length=255, blank=True, null=True)
    password_encrypted = models.TextField(_('رمز عبور (رمزنگاری شده)'), blank=True, null=True)
    email = models.EmailField(_('ایمیل'), blank=True, null=True)

    # اطلاعات اضافی
    domain = models.CharField(_('دامین'), max_length=255, blank=True, null=True, help_text='نام دامین (مثال: company.local)')
    notes = models.TextField(_('یادداشت‌ها'), blank=True, null=True, help_text='اطلاعات تکمیلی')

    # وضعیت و امنیت
    security_level = models.CharField(_('سطح امنیت'), max_length=10, choices=SECURITY_LEVEL_CHOICES, default='medium')
    status = models.CharField(_('وضعیت'), max_length=10, choices=STATUS_CHOICES, default='active')
    last_password_change = models.DateField(_('آخرین تغییر رمز'), blank=True, null=True)
    password_expiry = models.DateField(_('تاریخ انقضای رمز'), blank=True, null=True)

    # فراداده
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name=_('ایجاد شده توسط'), null=True, related_name='created_credentials')
    created_at = models.DateTimeField(_('تاریخ ایجاد'), auto_now_add=True)
    updated_at = models.DateTimeField(_('آخرین بروزرسانی'), auto_now=True)

    class Meta:
        verbose_name = _('اطلاعات دسترسی')
        verbose_name_plural = _('اطلاعات دسترسی‌ها')
        ordering = ['-security_level', 'category', 'title']

    def __str__(self):
        branch_name = f" [{self.branch}]" if self.branch else ""
        return f"{self.title}{branch_name}"

    @property
    def password(self):
        """دریافت رمز عبور رمزگشایی شده"""
        return decrypt_value(self.password_encrypted)

    @password.setter
    def password(self, value):
        """ذخیره رمز عبور رمزنگاری شده"""
        self.password_encrypted = encrypt_value(value) if value else ''

    def save(self, *args, **kwargs):
        # اگر رمز جدید رمزنگاری نشده باشد، رمزنگاری کن
        if self.password_encrypted and not self.password_encrypted.startswith(signer.sign('')):
            try:
                decrypt_value(self.password_encrypted)
            except Exception:
                self.password_encrypted = encrypt_value(self.password_encrypted)
        super().save(*args, **kwargs)

    def log_access(self, user, access_type='view', ip_address=None):
        """ثبت لاگ دسترسی"""
        CredentialLog.objects.create(
            credential=self,
            user=user,
            access_type=access_type,
            ip_address=ip_address or '',
        )

    def get_security_badge(self):
        """نمایش badge سطح امنیت"""
        badges = {
            'low': '<span class="badge badge-success">🟢 عادی</span>',
            'medium': '<span class="badge badge-warning">🟡 متوسط</span>',
            'high': '<span class="badge badge-danger" style="background:#f97316">🟠 حساس</span>',
            'critical': '<span class="badge badge-danger">🔴 بحرانی</span>',
        }
        return badges.get(self.security_level, '')


class CredentialAccess(models.Model):
    """کنترل دسترسی به اطلاعات"""

    ACCESS_LEVEL_CHOICES = [
        ('view', 'مشاهده (فقط خواندن)'),
        ('copy', 'مشاهده + کپی رمز'),
        ('edit', 'مشاهده + کپی + ویرایش'),
        ('full', 'دسترسی کامل'),
    ]

    credential = models.ForeignKey(Credential, on_delete=models.CASCADE, verbose_name=_('اطلاعات دسترسی'), related_name='access_entries')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('کاربر'), null=True, blank=True, related_name='credential_accesses')
    group = models.ForeignKey('auth.Group', on_delete=models.CASCADE, verbose_name=_('گروه'), null=True, blank=True, related_name='credential_accesses')
    access_level = models.CharField(_('سطح دسترسی'), max_length=10, choices=ACCESS_LEVEL_CHOICES, default='view')
    granted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name=_('اعطا شده توسط'), null=True, related_name='granted_credentials')
    granted_at = models.DateTimeField(_('تاریخ اعطا'), auto_now_add=True)
    note = models.TextField(_('یادداشت'), blank=True, null=True)

    class Meta:
        verbose_name = _('دسترسی')
        verbose_name_plural = _('دسترسی‌ها')
        unique_together = ['credential', 'user']  # هر کاربر فقط یه بار به هر credential دسترسی داشته باشه

    def __str__(self):
        target = self.user.get_full_name() or self.user.username if self.user else f"گروه: {self.group}"
        return f"{target} → {self.credential.title} ({self.get_access_level_display()})"

    def save(self, *args, **kwargs):
        if not self.user and not self.group:
            raise ValueError('باید حداقل یکی از کاربر یا گروه مشخص شود')
        super().save(*args, **kwargs)


class CredentialLog(models.Model):
    """لاگ دسترسی به اطلاعات"""

    ACCESS_TYPE_CHOICES = [
        ('view', 'مشاهده'),
        ('copy_password', 'کپی رمز'),
        ('edit', 'ویرایش'),
        ('create', 'ایجاد'),
        ('delete', 'حذف'),
        ('grant_access', 'اعطای دسترسی'),
        ('revoke_access', 'لغو دسترسی'),
    ]

    credential = models.ForeignKey(Credential, on_delete=models.CASCADE, verbose_name=_('اطلاعات دسترسی'), related_name='logs')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name=_('کاربر'), null=True)
    access_type = models.CharField(_('نوع دسترسی'), max_length=20, choices=ACCESS_TYPE_CHOICES)
    ip_address = models.GenericIPAddressField(_('آدرس IP'), blank=True, null=True)
    user_agent = models.TextField(_('مرورگر'), blank=True, null=True)
    details = models.TextField(_('جزئیات'), blank=True, null=True)
    created_at = models.DateTimeField(_('زمان'), auto_now_add=True)

    class Meta:
        verbose_name = _('لاگ دسترسی')
        verbose_name_plural = _('لاگ‌های دسترسی')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} - {self.get_access_type_display()} - {self.credential.title} ({self.created_at})"
