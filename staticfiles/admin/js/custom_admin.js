// ============================================
// CUSTOM ADMIN JS - POPUP & UI ENHANCEMENTS
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    console.log('Custom Admin JS loaded!');
    
    // 1. Fix Add buttons - make them open in popup
    setupAddButtons();
    
    // 2. If opened as popup - add close button
    if (window.location.search.includes('_popup=1') || window.opener) {
        setupPopupMode();
    }
    
    // 3. Make form inputs more visible
    enhanceFormInputs();
    
    // 4. Translate some English elements to Persian
    translateToPersian();
});

// ============================================
// SETUP ADD BUTTONS FOR POPUP
// ============================================
function setupAddButtons() {
    // Find all links that go to /add/ pages
    const addLinks = document.querySelectorAll('a[href*="/add/"]');
    
    addLinks.forEach(function(link) {
        // Skip if already has our handler
        if (link.dataset.popupSetup) return;
        link.dataset.popupSetup = 'true';
        
        link.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const url = this.href;
            openFormPopup(url);
        });
        
        // Make sure the link is visible
        link.style.display = 'inline-flex';
        link.style.visibility = 'visible';
        link.style.opacity = '1';
    });
    
    // Also look for buttons with "Add" text
    const addButtons = document.querySelectorAll('button, a, span');
    addButtons.forEach(function(btn) {
        const text = btn.textContent.toLowerCase().trim();
        if ((text === 'add' || text === 'افزودن' || text === 'اضافه کردن') && 
            btn.tagName === 'A' && btn.href && btn.href.includes('add')) {
            if (!btn.dataset.popupSetup) {
                btn.dataset.popupSetup = 'true';
                btn.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    openFormPopup(this.href);
                });
            }
        }
    });
}

// ============================================
// OPEN FORM IN POPUP WINDOW
// ============================================
function openFormPopup(url) {
    // Add _popup parameter
    const separator = url.includes('?') ? '&' : '?';
    const popupUrl = url + separator + '_popup=1';
    
    const width = Math.min(900, window.screen.width * 0.7);
    const height = Math.min(700, window.screen.height * 0.7);
    const left = (screen.width - width) / 2;
    const top = (screen.height - height) / 2;
    
    const popup = window.open(
        popupUrl,
        'admin_form_popup',
        'width=' + width + ',height=' + height + ',left=' + left + ',top=' + top + ',scrollbars=yes,resizable=yes'
    );
    
    if (popup) {
        popup.focus();
    }
    
    // Refresh parent when popup closes
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
    // Add body class
    document.body.classList.add('popup-mode');
    
    // Add close button
    const closeBtn = document.createElement('button');
    closeBtn.innerHTML = '✕ بستن';
    closeBtn.className = 'popup-close-btn';
    closeBtn.onclick = function() {
        if (window.opener) {
            window.opener.location.reload();
        }
        window.close();
    };
    document.body.appendChild(closeBtn);
    
    // Hide sidebar elements
    const sidebars = document.querySelectorAll('[class*="sidebar"], aside, nav');
    sidebars.forEach(function(el) {
        el.style.display = 'none';
    });
    
    // Make main content full width
    const mainContent = document.querySelector('#content, main, .main');
    if (mainContent) {
        mainContent.style.maxWidth = '100%';
        mainContent.style.width = '100%';
        mainContent.style.margin = '0';
        mainContent.style.padding = '20px';
    }
}

// ============================================
// ENHANCE FORM INPUTS
// ============================================
function enhanceFormInputs() {
    // Add visible borders to all inputs
    const inputs = document.querySelectorAll('input, textarea, select');
    inputs.forEach(function(input) {
        if (input.type !== 'hidden' && input.type !== 'checkbox' && input.type !== 'radio') {
            input.style.backgroundColor = '#0d1117';
            input.style.borderColor = '#30363d';
            input.style.color = '#f0f6fc';
            input.style.border = '2px solid #30363d';
        }
    });
}

// ============================================
// TRANSLATE TO PERSIAN
// ============================================
function translateToPersian() {
    // Translate common English elements
    const translations = {
        'Add': 'افزودن',
        'Change': 'تغییر',
        'Delete': 'حذف',
        'Save': 'ذخیره',
        'Save and add another': 'ذخیره و اضافه کردن',
        'Save and view': 'ذخیره و مشاهده',
        'Search': 'جستجو',
        'Type to search': 'تایپ کنید...',
        'Home': 'خانه',
        'Authentication and Authorization': 'احراز هویت و مجوز',
        'Groups': 'گروه‌ها',
        'Users': 'کاربران',
        'Show': 'نمایش',
        'History': 'تاریخچه',
        'View on site': 'مشاهده در سایت',
        'Log out': 'خروج',
        'Password': 'رمز عبور',
        'Username': 'نام کاربری',
        'Email': 'ایمیل',
        'First name': 'نام',
        'Last name': 'نام خانوادگی',
        'Permissions': 'مجوزها',
        'Active': 'فعال',
        'Date joined': 'تاریخ عضویت',
    };
    
    // Apply translations
    Object.keys(translations).forEach(function(english) {
        const elements = document.querySelectorAll('*');
        elements.forEach(function(el) {
            if (el.childNodes.length === 1 && el.childNodes[0].nodeType === 3) {
                if (el.textContent.trim() === english) {
                    el.textContent = translations[english];
                }
            }
        });
    });
}
