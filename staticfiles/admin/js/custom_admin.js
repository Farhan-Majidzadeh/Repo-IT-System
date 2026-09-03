// ============================================
// CUSTOM ADMIN JS - FULL PERSIAN TRANSLATION
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    console.log('Custom Admin JS loaded!');
    
    // 1. Translate all English text to Persian
    translateToPersian();
    
    // 2. Fix Add buttons
    setupAddButtons();
    
    // 3. Hide sidebar chevrons
    hideSidebarChevrons();
    
    // 4. Setup mobile sidebar toggle
    setupMobileSidebar();
    
    // 5. Popup mode
    if (window.location.search.includes('_popup=1') || window.opener) {
        setupPopupMode();
    }
    
    // Run translation after a delay for dynamic content
    setTimeout(translateToPersian, 1000);
    setTimeout(translateToPersian, 2000);
    setTimeout(hideSidebarChevrons, 1000);
    setTimeout(hideSidebarChevrons, 2000);
});

// ============================================
// COMPLETE PERSIAN TRANSLATIONS
// ============================================
function translateToPersian() {
    const translations = {
        // Navigation & Header
        'Home': 'خانه',
        'All applications': 'همه برنامه‌ها',
        'Search apps and models': 'جستجو در برنامه‌ها و مدل‌ها',
        'Type to search': 'تایپ کنید...',
        
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
// MOBILE SIDEBAR TOGGLE
// ============================================
function setupMobileSidebar() {
    // Create hamburger button
    var toggleBtn = document.createElement('button');
    toggleBtn.className = 'sidebar-toggle';
    toggleBtn.innerHTML = '<div class="hamburger"><span></span><span></span><span></span></div>';
    toggleBtn.setAttribute('aria-label', 'باز کردن منو');
    document.body.appendChild(toggleBtn);

    // Create overlay
    var overlay = document.createElement('div');
    overlay.className = 'sidebar-overlay';
    document.body.appendChild(overlay);

    // Get sidebar
    var sidebar = document.getElementById('nav-sidebar');
    if (!sidebar) return;

    // Toggle sidebar
    function toggleSidebar() {
        var isOpen = sidebar.classList.contains('mobile-open');
        
        if (isOpen) {
            sidebar.classList.remove('mobile-open');
            overlay.classList.remove('active');
            toggleBtn.classList.remove('active');
            document.body.style.overflow = '';
        } else {
            sidebar.classList.add('mobile-open');
            overlay.classList.add('active');
            toggleBtn.classList.add('active');
            document.body.style.overflow = 'hidden';
        }
    }

    // Close sidebar
    function closeSidebar() {
        sidebar.classList.remove('mobile-open');
        overlay.classList.remove('active');
        toggleBtn.classList.remove('active');
        document.body.style.overflow = '';
    }

    // Event listeners
    toggleBtn.addEventListener('click', toggleSidebar);
    overlay.addEventListener('click', closeSidebar);

    // Close on ESC key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && sidebar.classList.contains('mobile-open')) {
            closeSidebar();
        }
    });

    // Close sidebar when clicking a link on mobile
    sidebar.querySelectorAll('a').forEach(function(link) {
        link.addEventListener('click', function() {
            if (window.innerWidth < 1024) {
                closeSidebar();
            }
        });
    });

    // Handle resize - close sidebar if window becomes desktop size
    window.addEventListener('resize', function() {
        if (window.innerWidth >= 1024) {
            closeSidebar();
        }
    });

    console.log('Mobile sidebar initialized!');
}

// ============================================
// HIDE SIDEBAR CHEVRONS
// ============================================
function hideSidebarChevrons() {
    // Find all h2 elements in the sidebar that contain chevron_right icon
    document.querySelectorAll('#nav-sidebar h2').forEach(function(h2) {
        var chevronSpan = h2.querySelector('.material-symbols-outlined');
        if (chevronSpan && chevronSpan.textContent.trim() === 'chevron_right') {
            chevronSpan.style.display = 'none';
            chevronSpan.style.width = '0';
            chevronSpan.style.height = '0';
            chevronSpan.style.margin = '0';
            chevronSpan.style.overflow = 'hidden';
        }
    });

    // حذف نام انگلیسی اپ‌ها از سایدبار
    document.querySelectorAll('#nav-sidebar-apps .text-xs').forEach(function(el) {
        var text = el.textContent.trim();
        // اگر متن فقط انگلیسی باشد ( بدون حروف فارسی)
        var hasPersian = /[\u0600-\u06FF]/.test(text);
        if (!hasPersian && text.length > 0) {
            el.style.display = 'none';
        }
    });

    // حذف متن انگلیسی اضافه در کنار عناوین
    document.querySelectorAll('#nav-sidebar h2 span.text-xs').forEach(function(el) {
        el.style.display = 'none';
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
