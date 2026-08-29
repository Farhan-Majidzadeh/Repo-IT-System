from django.db import models
from django.core.validators import MinLengthValidator
from django.utils.text import slugify
import uuid


class Department(models.Model):
    code = models.CharField(max_length=20, unique=True, editable=False)
    name = models.CharField(max_length=100)
    building = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.code:
            base_code = slugify(self.name)[:8].upper() or 'DEPT'
            self.code = f"{base_code}-{uuid.uuid4().hex[:4].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = 'بخش'
        verbose_name_plural = 'بخش‌ها'


class Personnel(models.Model):
    personnel_code = models.CharField(max_length=20, unique=True, editable=False)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    entry_date = models.DateField()
    settlement_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.personnel_code:
            base_code = 'PRSN'
            self.personnel_code = f"{base_code}-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.personnel_code} - {self.full_name}"

    class Meta:
        verbose_name = 'پرسنل'
        verbose_name_plural = 'پرسنل‌ها'


class PersonnelDepartment(models.Model):
    personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    entry_date = models.DateField()
    exit_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=True)

    class Meta:
        unique_together = ('personnel', 'department', 'entry_date')
        verbose_name = 'ارتباط پرسنل با بخش'
        verbose_name_plural = 'ارتباط پرسنل با بخش‌ها'

    def __str__(self):
        return f"{self.personnel} -> {self.department}"
