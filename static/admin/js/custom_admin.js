// Custom Admin JS - Popup/Modal for forms

document.addEventListener('DOMContentLoaded', function() {
    // On changelist pages - make Add buttons open in popup
    const addLinks = document.querySelectorAll('.add-link, .object-tools a[href*="add/"]');
    
    addLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const url = this.href;
            openFormPopup(url);
        });
    });

    // On change form pages - add close button if opened as popup
    if (window.location.search.includes('_popup=1') || window.opener) {
        addCloseButton();
        adjustFormForPopup();
    }
});

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
        'form_popup',
        'width=' + width + ',height=' + height + ',left=' + left + ',top=' + top + ',scrollbars=yes,resizable=yes'
    );
    
    // Focus the popup
    if (popup) {
        popup.focus();
    }
    
    // Refresh parent page when popup closes
    const checkClosed = setInterval(function() {
        if (popup && popup.closed) {
            clearInterval(checkClosed);
            window.location.reload();
        }
    }, 500);
}

function addCloseButton() {
    const closeBtn = document.createElement('button');
    closeBtn.innerHTML = '✕ بستن';
    closeBtn.className = 'popup-close-btn';
    closeBtn.style.cssText = 'position:fixed;top:10px;left:10px;z-index:9999;background:#ef4444;color:white;border:none;padding:8px 16px;border-radius:8px;cursor:pointer;font-size:14px;font-weight:bold;';
    closeBtn.onclick = function() {
        if (window.opener) {
            window.opener.location.reload();
        }
        window.close();
    };
    document.body.appendChild(closeBtn);
}

function adjustFormForPopup() {
    // Hide sidebar in popup mode
    const sidebar = document.querySelector('[class*="sidebar"], nav');
    if (sidebar) sidebar.style.display = 'none';
    
    // Make form more compact
    const content = document.querySelector('#content, .content, main');
    if (content) {
        content.style.maxWidth = '100%';
        content.style.padding = '20px';
    }
    
    // Add body class
    document.body.classList.add('popup-mode');
}
