// ============================================
// CUSTOM ADMIN JS - IT Management System
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    console.log('Custom Admin JS loaded!');

    // 1. Hide sidebar chevrons
    hideSidebarChevrons();

    // 2. Setup mobile sidebar toggle
    setupMobileSidebar();

    // 3. Translate specific UI elements (SAFE - targeted only)
    translateUI();

    // Re-run for dynamic content
    setTimeout(hideSidebarChevrons, 500);
    setTimeout(hideSidebarChevrons, 1500);
});

// ============================================
// SAFE TRANSLATION - Only specific known elements
// ============================================
function translateUI() {
    // Translate specific placeholders only
    var searchInputs = document.querySelectorAll('input[name="q"]');
    searchInputs.forEach(function(el) {
        if (!el.dataset.translated) {
            el.placeholder = 'جستجو کنید...';
            el.dataset.translated = 'true';
        }
    });

    // Translate header navigation
    document.querySelectorAll('.header-link').forEach(function(el) {
        var text = el.textContent.trim();
        if (text === 'View site') el.textContent = 'مشاهده سایت';
        if (text === 'Log out') el.textContent = 'خروج';
        if (text === 'Change password') el.textContent = 'تغییر رمز عبور';
    });

    // Translate breadcrumbs separator
    document.querySelectorAll('.breadcrumbs a, .breadcrumbs span').forEach(function(el) {
        var t = el.textContent.trim();
        if (t === 'Home') el.textContent = 'خانه';
    });
}

// ============================================
// HIDE SIDEBAR CHEVRONS
// ============================================
function hideSidebarChevrons() {
    // Hide chevron_right icons in sidebar
    document.querySelectorAll('#nav-sidebar h2').forEach(function(h2) {
        var spans = h2.querySelectorAll('.material-symbols-outlined');
        spans.forEach(function(span) {
            if (span.textContent.trim() === 'chevron_right') {
                span.style.display = 'none';
            }
        });
    });

    // Hide English app names from sidebar (keep only Persian)
    document.querySelectorAll('#nav-sidebar .text-xs, #nav-sidebar h2 .text-xs').forEach(function(el) {
        var text = el.textContent.trim();
        var hasPersian = /[\u0600-\u06FF]/.test(text);
        if (!hasPersian && text.length > 0) {
            el.style.display = 'none';
        }
    });
}

// ============================================
// MOBILE SIDEBAR TOGGLE
// ============================================
function setupMobileSidebar() {
    var sidebar = document.getElementById('nav-sidebar');
    if (!sidebar) return;

    // Don't setup on popup pages
    if (window.location.search.indexOf('_popup=') !== -1) return;

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

    function closeSidebar() {
        sidebar.classList.remove('mobile-open');
        overlay.classList.remove('active');
        toggleBtn.classList.remove('active');
        document.body.style.overflow = '';
    }

    toggleBtn.addEventListener('click', toggleSidebar);
    overlay.addEventListener('click', closeSidebar);

    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && sidebar.classList.contains('mobile-open')) {
            closeSidebar();
        }
    });

    // Close on link click (mobile)
    sidebar.querySelectorAll('a').forEach(function(link) {
        link.addEventListener('click', function() {
            if (window.innerWidth < 1024) closeSidebar();
        });
    });

    // Close on resize to desktop
    window.addEventListener('resize', function() {
        if (window.innerWidth >= 1024) closeSidebar();
    });

    console.log('Mobile sidebar initialized!');
}
