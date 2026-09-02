/**
 * Credential Admin - Password Toggle & Copy
 * فعال‌سازی نمایش/پنهان کردن رمز عبور در صفحه ادمین
 */
document.addEventListener('DOMContentLoaded', function() {
    // پیدا کردن فیلد رمز عبور
    const passwordField = document.querySelector('#id_password_encrypted');
    if (!passwordField) return;

    // ایجاد دکمه‌ها
    const container = document.createElement('div');
    container.style.cssText = 'display:flex; gap:8px; margin-top:8px; align-items:center;';

    // دکمه نمایش رمز
    const toggleBtn = document.createElement('button');
    toggleBtn.type = 'button';
    toggleBtn.className = 'button default';
    toggleBtn.innerHTML = '👁️ نمایش رمز';
    toggleBtn.style.cssText = 'background:#7c3aed; color:white; border:none; padding:6px 12px; border-radius:6px; cursor:pointer; font-size:13px;';

    // دکمه کپی
    const copyBtn = document.createElement('button');
    copyBtn.type = 'button';
    copyBtn.className = 'button default';
    copyBtn.innerHTML = '📋 کپی';
    copyBtn.style.cssText = 'background:#059669; color:white; border:none; padding:6px 12px; border-radius:6px; cursor:pointer; font-size:13px; display:none;';

    let isVisible = false;

    toggleBtn.addEventListener('click', function() {
        if (isVisible) {
            passwordField.type = 'password';
            passwordField.value = '';
            toggleBtn.innerHTML = '👁️ نمایش رمز';
            copyBtn.style.display = 'none';
            isVisible = false;
        } else {
            // دریافت رمز از سرور
            const credId = window.location.pathname.split('/').filter(x => x).pop();
            fetch(`/credentials/api/toggle-password/${credId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                },
            })
            .then(r => r.json())
            .then(data => {
                if (data.password) {
                    passwordField.type = 'text';
                    passwordField.value = data.password;
                    toggleBtn.innerHTML = '🙈 پنهان کردن';
                    if (data.can_copy) {
                        copyBtn.style.display = 'inline-block';
                    }
                    isVisible = true;
                } else {
                    alert(data.error || 'خطا در دریافت رمز');
                }
            })
            .catch(err => {
                alert('خطا در اتصال به سرور');
            });
        }
    });

    copyBtn.addEventListener('click', function() {
        if (passwordField.value) {
            navigator.clipboard.writeText(passwordField.value).then(() => {
                copyBtn.innerHTML = '✅ کپی شد!';
                setTimeout(() => {
                    copyBtn.innerHTML = '📋 کپی';
                }, 2000);
            }).catch(() => {
                // fallback
                passwordField.select();
                document.execCommand('copy');
                copyBtn.innerHTML = '✅ کپی شد!';
                setTimeout(() => {
                    copyBtn.innerHTML = '📋 کپی';
                }, 2000);
            });
        }
    });

    container.appendChild(toggleBtn);
    container.appendChild(copyBtn);
    passwordField.parentNode.appendChild(container);
});
