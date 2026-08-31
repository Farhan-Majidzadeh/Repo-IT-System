from django.db import models
from django.core.validators import MinLengthValidator
from personnel.models import Personnel, Branch
from projects.models import Project
from django.utils.text import slugify
import uuid


class TicketCategory(models.Model):
    code = models.CharField(max_length=20, unique=True, editable=False)
    title = models.CharField(max_length=200)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    level = models.PositiveIntegerField(default=1)
    path = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.code:
            base_code = slugify(self.title)[:8].upper() or 'CAT'
            self.code = f"{base_code}-{uuid.uuid4().hex[:4].upper()}"
        if self.parent:
            self.level = self.parent.level + 1
            self.path = f"{self.parent.path}/{self.title}" if self.parent.path else self.title
        else:
            self.level = 1
            self.path = self.title
        super().save(*args, **kwargs)

    def __str__(self):
        return self.path

    class Meta:
        verbose_name = 'دسته‌بندی تیکت'
        verbose_name_plural = 'دسته‌بندی تیکت‌ها'


class Assignment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    category = models.ForeignKey(TicketCategory, on_delete=models.CASCADE)
    responsible_person = models.ForeignKey(Personnel, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True, verbose_name='شعبه مسئول')
    priority = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('project', 'category')
        verbose_name = 'تخصیص'
        verbose_name_plural = 'تخصیص‌ها'

    def __str__(self):
        return f"{self.project} - {self.category} -> {self.responsible_person}"


class Ticket(models.Model):
    PRIORITY_CHOICES = (('low', 'کم'), ('medium', 'متوسط'), ('high', 'بالا'), ('critical', 'بحرانی'))
    STATUS_CHOICES = (('open', 'باز'), ('in_progress', 'در حال انجام'), ('resolved', 'حل شده'), ('closed', 'بسته شده'))

    code = models.CharField(max_length=20, unique=True, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(TicketCategory, on_delete=models.SET_NULL, null=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
    requester = models.ForeignKey(Personnel, on_delete=models.CASCADE, related_name='requested_tickets')
    assigned_to = models.ForeignKey(Personnel, on_delete=models.SET_NULL, null=True, related_name='assigned_tickets')

    # شعبه‌ای که تیکت بهش مربوطه
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='شعبه')
    # واحد IT مقصد
    target_branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name='target_tickets', verbose_name='ارجاع به واحد IT')

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    deadline = models.DateField(blank=True, null=True)
    resolved_at = models.DateTimeField(blank=True, null=True)
    closed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.code:
            base_code = 'TKT'
            self.code = f"{base_code}-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.code} - {self.title}"

    class Meta:
        verbose_name = 'تیکت'
        verbose_name_plural = 'تیکت‌ها'


class TicketMessage(models.Model):
    MESSAGE_TYPES = (('text', 'متن'), ('file', 'فایل'), ('audio', 'صوت'))

    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(Personnel, on_delete=models.CASCADE)
    message = models.TextField(blank=True, null=True)
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPES, default='text')
    file_url = models.CharField(max_length=500, blank=True, null=True)
    file_name = models.CharField(max_length=200, blank=True, null=True)
    audio_url = models.CharField(max_length=500, blank=True, null=True)
    duration = models.PositiveIntegerField(blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ticket} - {self.sender} - {self.created_at}"

    class Meta:
        verbose_name = 'پیام تیکت'
        verbose_name_plural = 'پیام‌های تیکت'
