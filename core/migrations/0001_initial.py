# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='سیستم مدیریت IT', max_length=200, verbose_name='نام سایت')),
                ('subheader', models.CharField(default='پنل مدیریت جامع', max_length=200, verbose_name='زیرعنوان')),
                ('theme', models.CharField(choices=[('dark', 'تاریک'), ('light', 'روشن')], default='dark', max_length=20, verbose_name='تم')),
                ('primary_color', models.CharField(choices=[('purple', 'بنفش (پیش‌فرض)'), ('blue', 'آبی'), ('green', 'سبز'), ('red', 'قرمز'), ('orange', 'نارنجی'), ('teal', 'سبزآبی'), ('pink', 'صورتی'), ('indigo', 'نیلی')], default='purple', max_length=20, verbose_name='رنگ اصلی')),
                ('font', models.CharField(choices=[('Vazirmatn', 'وزیرمتن (پیش‌فرض)'), ('IRANSans', 'ایران‌سنس'), ('Tahoma', 'تاهوما'), ('B Nazanin', 'بی‌نازنین'), ('B Titr', 'بی‌تیتر'), ('Samim', 'سیمین'), ('Shabnam', 'شبنم'), ('Mj_Nava', ' MJ نوا')], default='Vazirmatn', max_length=50, verbose_name='فونت')),
                ('font_size', models.IntegerField(default=14, help_text='اندازه فونت پایه سایت', verbose_name='اندازه فونت (px)')),
                ('border_radius', models.IntegerField(default=8, help_text='میزان گردی گوشه المان‌ها', verbose_name='گردی گوشه‌ها (px)')),
                ('show_breadcrumbs', models.BooleanField(default=True, verbose_name='نمایش مسیر ناوبری')),
                ('show_logo', models.BooleanField(default=True, verbose_name='نمایش لوگو')),
                ('sidebar_compact', models.BooleanField(default=False, verbose_name='سایدبار فشرده')),
                ('custom_css', models.TextField(blank=True, help_text='کدهای CSS اضافی', null=True, verbose_name='CSS سفارشی')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'تنظیمات سایت',
                'verbose_name_plural': 'تنظیمات سایت',
                'ordering': ['-created_at'],
            },
        ),
    ]
