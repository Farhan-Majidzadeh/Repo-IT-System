// ============================================
// CUSTOM ADMIN JS - FULL PERSIAN TRANSLATION
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    console.log('Custom Admin JS loaded!');
    
    // 1. Translate all English text to Persian
    translateToPersian();
    
    // 2. Fix Add buttons
    setupAddButtons();
    
    // 3. Popup mode
    if (window.location.search.includes('_popup=1') || window.opener) {
        setupPopupMode();
    }
    
    // Run translation after a delay for dynamic content
    setTimeout(translateToPersian, 1000);
    setTimeout(translateToPersian, 2000);
});

// ============================================
// COMPLETE PERSIAN TRANSLATIONS
// ============================================
function translateToPersian() {
    const translations = {
        // Navigation & Header
        'Home': 'خانه',
        'All applications': 'همه برنامه‌ها',
        
        // Auth
        'Authentication and Authorization': 'احراز هویت و مجوز',
        'Groups': 'گروه‌ها',
        'Users': 'کاربران',
        'Log out': 'خروج',
        'Change password': 'تغییر رمز عبور',
        'View site': 'مشاهده سایت',
        'Welcome back to': 'خوش آمدید',
        
        // Buttons
        'Add': 'افزودن',
        'Save': 'ذخیره',
        'Save and add another': 'ذخیره و افزودن',
        'Save and view': 'ذخیره و مشاهده',
        'Delete': 'حذف',
        'Reset filters': 'پاک کردن فیلترها',
        'Search': 'جستجو',
        'Type to search': 'تایپ کنید...',
        
        // Filters
        'By status': 'بر اساس وضعیت',
        'By start date': 'بر اساس تاریخ شروع',
        'Any date': 'هر تاریخی',
        'Today': 'امروز',
        'Past 7 days': '۷ روز گذشته',
        'This month': 'این ماه',
        'This year': 'این سال',
        'This week': 'این هفته',
        'Past 30 days': '۳۰ روز گذشته',
        'Past 90 days': '۹۰ روز گذشته',
        
        // Empty states
        'No results found': 'نتیجه‌ای یافت نشد',
        'This page yielded into no results. Create a new item or reset your filters.':
            'هیچ نتیجه‌ای یافت نشد. یک آیتم جدید اضافه کنید یا فیلترها را پاک کنید.',
        
        // Actions
        'Show': 'نمایش',
        'History': 'تاریخچه',
        'View on site': 'مشاهده در سایت',
        
        // Login form
        'Username': 'نام کاربری',
        'Password': 'رمز عبور',
        'Log in': 'ورود',
        'Login': 'ورود',
        'Please correct the error below.': 'لطفاً خطای زیر را اصلاح کنید.',
        'Please enter the correct username and password for a staff account. Note that both fields may be case-sensitive.':
            'لطفاً نام کاربری و رمز عبور صحیح را وارد کنید.',
        
        // Form labels
        'Email': 'ایمیل',
        'First name': 'نام',
        'Last name': 'نام خانوادگی',
        'Permissions': 'مجوزها',
        'Active': 'فعال',
        'Date joined': 'تاریخ عضویت',
        'Staff status': 'وضعیت کارمند',
        'Superuser status': 'وضعیت مدیر',
        'Personal info': 'اطلاعات شخصی',
        'Important dates': 'تاریخ‌های مهم',
        
        // Status
        'All': 'همه',
        'Selected': 'انتخاب شده',
        
        // Pagination
        'Show all': 'نمایش همه',
        'questions': 'سوالات',
        
        // Errors
        'Error': 'خطا',
        'Errors': 'خطاها',
        
        // Misc
        'date': 'تاریخ',
        'week': 'هفته',
        'today': 'امروز',
        'month': 'ماه',
        'year': 'سال',
    };
    
    // Apply translations to all text nodes
    const walker = document.createTreeWalker(
        document.body,
        NodeFilter.SHOW_TEXT,
        null,
        false
    );
    
    const textNodes = [];
    while (walker.nextNode()) {
        textNodes.push(walker.currentNode);
    }
    
    textNodes.forEach(function(node) {
        const text = node.textContent.trim();
        if (translations[text]) {
            node.textContent = node.textContent.replace(text, translations[text]);
        }
    });
    
    // Translate placeholders
    document.querySelectorAll('input[placeholder], textarea[placeholder]').forEach(function(el) {
        if (translations[el.placeholder]) {
            el.placeholder = translations[el.placeholder];
        }
    });
    
    // Translate attributes (title, aria-label)
    document.querySelectorAll('[title]').forEach(function(el) {
        if (translations[el.title]) {
            el.title = translations[el.title];
        }
    });
    
    document.querySelectorAll('[aria-label]').forEach(function(el) {
        if (translations[el.getAttribute('aria-label')]) {
            el.setAttribute('aria-label', translations[el.getAttribute('aria-label')]);
        }
    });
}

// ============================================
// SETUP ADD BUTTONS FOR POPUP
// ============================================
function setupAddButtons() {
    const addLinks = document.querySelectorAll('a[href*="/add/"]');
    addLinks.forEach(function(link) {
        if (link.dataset.popupSetup) return;
        link.dataset.popupSetup = 'true';
        link.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            openFormPopup(this.href);
        });
        link.style.display = 'inline-flex';
        link.style.visibility = 'visible';
        link.style.opacity = '1';
    });
}

// ============================================
// OPEN FORM IN POPUP
// ============================================
function openFormPopup(url) {
    const separator = url.includes('?') ? '&' : '?';
    const popupUrl = url + separator + '_popup=1';
    const width = Math.min(900, window.screen.width * 0.7);
    const height = Math.min(700, window.screen.height * 0.7);
    const left = (screen.width - width) / 2;
    const top = (screen.height - height) / 2;
    const popup = window.open(popupUrl, 'admin_form_popup',
        'width=' + width + ',height=' + height + ',left=' + left + ',top=' + top + ',scrollbars=yes,resizable=yes'
    );
    if (popup) popup.focus();
    const checkClosed = setInterval(function() {
        if (popup && popup.closed) {
            clearInterval(checkClosed);
            window.location.reload();
        }
    }, 500);
}

// ============================================
// SETUP POPUP MODE
// ============================================
function setupPopupMode() {
    document.body.classList.add('popup-mode');
    const closeBtn = document.createElement('button');
    closeBtn.innerHTML = '✕ بستن';
    closeBtn.className = 'popup-close-btn';
    closeBtn.onclick = function() {
        if (window.opener) window.opener.location.reload();
        window.close();
    };
    document.body.appendChild(closeBtn);
    document.querySelectorAll('[class*="sidebar"], aside, nav').forEach(function(el) {
        el.style.display = 'none';
    });
}
