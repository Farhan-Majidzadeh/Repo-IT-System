# Generated manually for credentials app

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_group_name_max_length'),
        ('personnel', '0004_branch_personnel_is_it_specialist_department_branch_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CredentialCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='نام دسته‌بندی')),
                ('category_type', models.CharField(choices=[('domain', 'دامین / Active Directory'), ('mail', 'سرویس ایمیل'), ('server', 'سرور'), ('network', 'تجهیزات شبکه'), ('printer', 'چاپگر'), ('website', 'وب‌سایت / پنل'), ('database', 'پایگاه داده'), ('vpn', 'VPN'), ('backup', 'پشتیبان‌گیری'), ('cloud', 'سرویس ابری'), ('software', 'نرم‌افزار'), ('camera', 'دوربین مداربسته'), ('ups', 'UPS / برق اضطراری'), ('other', 'سایر')], default='other', max_length=20, verbose_name='نوع')),
                ('icon', models.CharField(default='vpn_key', help_text='نام آیکون Material Icons', max_length=50, verbose_name='آیکون Material')),
                ('description', models.TextField(blank=True, null=True, verbose_name='توضیحات')),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال')),
                ('order', models.IntegerField(default=0, verbose_name='ترتیب')),
            ],
            options={
                'verbose_name': 'دسته‌بندی دسترسی',
                'verbose_name_plural': 'دسته‌بندی‌های دسترسی',
                'ordering': ['order', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Credential',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='مثال: لاگین دامین مشهد', max_length=200, verbose_name='عنوان')),
                ('hostname', models.CharField(blank=True, help_text='آدرس IP یا hostname سرور/دستگاه', max_length=255, null=True, verbose_name='Hostname / IP')),
                ('port', models.CharField(blank=True, help_text='پورت اتصال (مثال: 3389, 443)', max_length=10, null=True, verbose_name='پورت')),
                ('url', models.URLField(blank=True, null=True, verbose_name='آدرس URL')),
                ('username', models.CharField(blank=True, max_length=255, null=True, verbose_name='نام کاربری')),
                ('password_encrypted', models.TextField(blank=True, null=True, verbose_name='رمز عبور (رمزنگاری شده)')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='ایمیل')),
                ('domain', models.CharField(blank=True, help_text='نام دامین (مثال: company.local)', max_length=255, null=True, verbose_name='دامین')),
                ('notes', models.TextField(blank=True, help_text='اطلاعات تکمیلی', null=True, verbose_name='یادداشت‌ها')),
                ('security_level', models.CharField(choices=[('low', '🟢 عادی'), ('medium', '🟡 متوسط'), ('high', '🟠 حساس'), ('critical', '🔴 بحرانی')], default='medium', max_length=10, verbose_name='سطح امنیت')),
                ('status', models.CharField(choices=[('active', 'فعال'), ('inactive', 'غیرفعال'), ('expired', 'منقضی شده'), ('archived', 'بایگانی شده')], default='active', max_length=10, verbose_name='وضعیت')),
                ('last_password_change', models.DateField(blank=True, null=True, verbose_name='آخرین تغییر رمز')),
                ('password_expiry', models.DateField(blank=True, null=True, verbose_name='تاریخ انقضای رمز')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='آخرین بروزرسانی')),
                ('branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='credentials', to='personnel.branch', verbose_name='شعبه')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='credentials', to='credentials.credentialcategory', verbose_name='دسته‌بندی')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_credentials', to=settings.AUTH_USER_MODEL, verbose_name='ایجاد شده توسط')),
            ],
            options={
                'verbose_name': 'اطلاعات دسترسی',
                'verbose_name_plural': 'اطلاعات دسترسی‌ها',
                'ordering': ['-security_level', 'category', 'title'],
            },
        ),
        migrations.CreateModel(
            name='CredentialAccess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_level', models.CharField(choices=[('view', 'مشاهده (فقط خواندن)'), ('copy', 'مشاهده + کپی رمز'), ('edit', 'مشاهده + کپی + ویرایش'), ('full', 'دسترسی کامل')], default='view', max_length=10, verbose_name='سطح دسترسی')),
                ('granted_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ اعطا')),
                ('note', models.TextField(blank=True, null=True, verbose_name='یادداشت')),
                ('credential', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='access_entries', to='credentials.credential', verbose_name='اطلاعات دسترسی')),
                ('granted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='granted_credentials', to=settings.AUTH_USER_MODEL, verbose_name='اعطا شده توسط')),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='credential_accesses', to='auth.group', verbose_name='گروه')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='credential_accesses', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'دسترسی',
                'verbose_name_plural': 'دسترسی‌ها',
                'unique_together': {('credential', 'user')},
            },
        ),
        migrations.CreateModel(
            name='CredentialLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_type', models.CharField(choices=[('view', 'مشاهده'), ('copy_password', 'کپی رمز'), ('edit', 'ویرایش'), ('create', 'ایجاد'), ('delete', 'حذف'), ('grant_access', 'اعطای دسترسی'), ('revoke_access', 'لغو دسترسی')], max_length=20, verbose_name='نوع دسترسی')),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True, verbose_name='آدرس IP')),
                ('user_agent', models.TextField(blank=True, null=True, verbose_name='مرورگر')),
                ('details', models.TextField(blank=True, null=True, verbose_name='جزئیات')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='زمان')),
                ('credential', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='credentials.credential', verbose_name='اطلاعات دسترسی')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'لاگ دسترسی',
                'verbose_name_plural': 'لاگ‌های دسترسی',
                'ordering': ['-created_at'],
            },
        ),
    ]
