// Custom Admin JS - Popup/Modal for forms

document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on a popup page
    const isPopup = window.location.search.includes('_popup=1');

    if (isPopup) {
        // Add popup container class
        document.body.classList.add('popup-mode');

        // Remove sidebar and header for cleaner popup
        const sidebar = document.querySelector('.sidebar, [class*="sidebar"]');
        const header = document.querySelector('header, [class*="header"]');

        if (sidebar) sidebar.style.display = 'none';
        if (header) header.style.display = 'none';

        // Add close button
        const closeBtn = document.createElement('button');
        closeBtn.innerHTML = '✕';
        closeBtn.className = 'popup-close-btn';
        closeBtn.onclick = function() {
            window.close();
        };
        document.body.appendChild(closeBtn);
    }

    // Add popup class to body
    document.body.classList.add('custom-admin-theme');
});

// Function to open popup
function openPopup(url, title) {
    const width = 800;
    const height = 600;
    const left = (screen.width - width) / 2;
    const top = (screen.height - height) / 2;

    window.open(
        url + '?_popup=1',
        title,
        `width=${width},height=${height},left=${left},top=${top},scrollbars=yes,resizable=yes`
    );
}
