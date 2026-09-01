from django.db import models
from django.utils.translation import gettext_lazy as _


class SiteSettings(models.Model):
    """تنظیمات ظاهری سایت"""
    
    THEME_CHOICES = [
        ('dark', 'تاریک'),
        ('light', 'روشن'),
    ]
    
    FONT_CHOICES = [
        ('Vazirmatn', 'وزیرمتن (پیش‌فرض)'),
        ('IRANSans', 'ایران‌سنس'),
        ('Tahoma', 'تاهوما'),
        ('B Nazanin', 'بی‌نازنین'),
        ('B Titr', 'بی‌تیتر'),
        ('Samim', 'سیمین'),
        ('Shabnam', 'شبنم'),
        ('Mj_Nava', ' MJ نوا'),
    ]
    
    PRIMARY_COLOR_CHOICES = [
        ('purple', 'بنفش (پیش‌فرض)'),
        ('blue', 'آبی'),
        ('green', 'سبز'),
        ('red', 'قرمز'),
        ('orange', 'نارنجی'),
        ('teal', 'سبزآبی'),
        ('pink', 'صورتی'),
        ('indigo', 'نیلی'),
    ]

    name = models.CharField(_('نام سایت'), max_length=200, default='سیستم مدیریت IT')
    subheader = models.CharField(_('زیرعنوان'), max_length=200, default='پنل مدیریت جامع')
    
    theme = models.CharField(_('تم'), max_length=20, choices=THEME_CHOICES, default='dark')
    primary_color = models.CharField(_('رنگ اصلی'), max_length=20, choices=PRIMARY_COLOR_CHOICES, default='purple')
    font = models.CharField(_('فونت'), max_length=50, choices=FONT_CHOICES, default='Vazirmatn')
    
    font_size = models.IntegerField(_('اندازه فونت (px)'), default=14, help_text='اندازه فونت پایه سایت')
    border_radius = models.IntegerField(_('گردی گوشه‌ها (px)'), default=8, help_text='میزان گردی گوشه المان‌ها')
    
    show_breadcrumbs = models.BooleanField(_('نمایش مسیر ناوبری'), default=True)
    show_logo = models.BooleanField(_('نمایش لوگو'), default=True)
    sidebar_compact = models.BooleanField(_('سایدبار فشرده'), default=False)
    
    custom_css = models.TextField(_('CSS سفارشی'), blank=True, null=True, help_text='کدهای CSS اضافی')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('تنظیمات سایت')
        verbose_name_plural = _('تنظیمات سایت')
        ordering = ['-created_at']

    def __str__(self):
        return f"تنظیمات ظاهری - {self.name}"

    def save(self, *args, **kwargs):
        # فقط یه رکورد تنظیمات وجود داشته باشه
        if not self.pk and SiteSettings.objects.exists():
            existing = SiteSettings.objects.first()
            self.pk = existing.pk
        super().save(*args, **kwargs)

    @classmethod
    def get_instance(cls):
        """دریافت یا ساخت تنظیمات پیش‌فرض"""
        obj, _ = cls.objects.get_or_create(
            pk=1,
            defaults={
                'name': 'سیستم مدیریت IT',
                'subheader': 'پنل مدیریت جامع',
                'theme': 'dark',
                'primary_color': 'purple',
                'font': 'Vazirmatn',
                'font_size': 14,
                'border_radius': 8,
            }
        )
        return obj

    def get_color_values(self):
        """دریافت مقادیر رنگ بر اساس رنگ انتخاب شده"""
        colors = {
            'purple': {
                '50': '250 245 255', '100': '244 231 255', '200': '238 217 255',
                '300': '224 186 255', '400': '206 147 255', '500': '187 107 255',
                '600': '168 85 247', '700': '147 51 234', '800': '126 34 206', '900': '107 27 183',
            },
            'blue': {
                '50': '239 246 255', '100': '219 234 254', '200': '191 219 254',
                '300': '147 197 253', '400': '96 165 250', '500': '59 130 246',
                '600': '37 99 235', '700': '29 78 216', '800': '30 64 175', '900': '30 58 138',
            },
            'green': {
                '50': '240 253 244', '100': '220 252 231', '200': '187 247 208',
                '300': '134 239 172', '400': '74 222 128', '500': '34 197 94',
                '600': '22 163 74', '700': '21 128 61', '800': '22 101 52', '900': '20 83 45',
            },
            'red': {
                '50': '254 242 242', '100': '254 226 226', '200': '254 202 202',
                '300': '252 165 165', '400': '248 113 113', '500': '239 68 68',
                '600': '220 38 38', '700': '185 28 28', '800': '153 27 27', '900': '127 29 29',
            },
            'orange': {
                '50': '255 247 237', '100': '255 237 213', '200': '254 215 170',
                '300': '253 186 116', '400': '251 146 60', '500': '249 115 22',
                '600': '234 88 12', '700': '194 65 12', '800': '154 52 18', '900': '124 45 18',
            },
            'teal': {
                '50': '240 253 250', '100': '204 251 241', '200': '153 246 228',
                '300': '94 234 212', '400': '45 212 191', '500': '20 184 166',
                '600': '13 148 136', '700': '15 118 110', '800': '17 94 89', '900': '19 78 74',
            },
            'pink': {
                '50': '252 231 243', '100': '251 207 232', '200': '249 168 212',
                '300': '244 114 182', '400': '236 72 153', '500': '219 39 119',
                '600': '190 24 93', '700': '157 23 77', '800': '131 24 65', '900': '107 20 54',
            },
            'indigo': {
                '50': '238 242 255', '100': '224 231 255', '200': '199 210 254',
                '300': '165 180 252', '400': '129 140 248', '500': '99 102 241',
                '600': '79 70 229', '700': '67 56 202', '800': '55 48 163', '900': '49 46 129',
            },
        }
        return colors.get(self.primary_color, colors['purple'])

    def get_font_family(self):
        """دریافت font-family بر اساس فونت انتخاب شده"""
        fonts = {
            'Vazirmatn': "'Vazirmatn', 'Tahoma', sans-serif",
            'IRANSans': "'IRANSans', 'Tahoma', sans-serif",
            'Tahoma': "'Tahoma', 'Arial', sans-serif",
            'B Nazanin': "'B Nazanin', 'Tahoma', sans-serif",
            'B Titr': "'B Titr', 'Tahoma', sans-serif",
            'Samim': "'Samim', 'Tahoma', sans-serif",
            'Shabnam': "'Shabnam', 'Tahoma', sans-serif",
            'Mj_Nava': "'MJ Nava', 'Tahoma', sans-serif",
        }
        return fonts.get(self.font, fonts['Vazirmatn'])

    def get_dynamic_css(self):
        """تولید CSS پویا بر اساس تنظیمات"""
        colors = self.get_color_values()
        font_family = self.get_font_family()
        border_radius = self.border_radius
        font_size = self.font_size

        bg_primary = '#1e1e2e' if self.theme == 'dark' else '#ffffff'
        bg_secondary = '#2d2d3f' if self.theme == 'dark' else '#f8f9fa'
        text_primary = '#e6edf3' if self.theme == 'dark' else '#1a1a2e'
        text_secondary = '#8b949e' if self.theme == 'dark' else '#6b7280'

        css = f"""
        :root {{
            --primary-rgb: {colors.get('500', '187 107 255')};
            --primary-50: rgb({colors.get('50', '250 245 255')});
            --primary-100: rgb({colors.get('100', '244 231 255')});
            --primary-500: rgb({colors.get('500', '187 107 255')});
            --primary-600: rgb({colors.get('600', '168 85 247')});
            --primary-700: rgb({colors.get('700', '147 51 234')});
            --bg-primary: {bg_primary};
            --bg-secondary: {bg_secondary};
            --text-primary: {text_primary};
            --text-secondary: {text_secondary};
            --font-family: {font_family};
            --border-radius: {border_radius}px;
            --font-size: {font_size}px;
        }}
        * {{ font-family: {font_family} !important; }}
        body {{ font-size: {font_size}px; direction: rtl; text-align: right; }}
        """

        if self.custom_css:
            css += f"\n/* CSS سفارشی */\n{self.custom_css}"

        return css

    def get_font_url(self):
        """دریافت URL فونت Google Fonts"""
        fonts = {
            'Vazirmatn': 'https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700&display=swap',
            'IRANSans': 'https://fonts.googleapis.com/css2?family=IRANSans:wght@300;400;500;600;700&display=swap',
            'Samim': 'https://fonts.googleapis.com/css2?family=Samim:wght@300;400;500;600;700&display=swap',
            'Shabnam': 'https://fonts.googleapis.com/css2?family=Shabnam:wght@300;400;500;600;700&display=swap',
        }
        return fonts.get(self.font, '')
