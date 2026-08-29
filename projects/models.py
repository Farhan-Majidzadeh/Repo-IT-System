from django.db import models
from django.utils.text import slugify
import uuid


class Project(models.Model):
    code = models.CharField(max_length=20, unique=True, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.code:
            # Auto-generate code from name + random suffix
            base_code = slugify(self.name)[:8].upper() or 'PRJ'
            self.code = f"{base_code}-{uuid.uuid4().hex[:4].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = 'پروژه'
        verbose_name_plural = 'پروژه‌ها'
