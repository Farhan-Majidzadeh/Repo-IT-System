import json
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import Credential, CredentialAccess, CredentialLog


@staff_member_required
@require_POST
def toggle_password(request, credential_id):
    """API برای نمایش/پنهان کردن رمز عبور"""
    try:
        credential = Credential.objects.get(pk=credential_id)
    except Credential.DoesNotExist:
        return JsonResponse({'error': 'یافت نشد'}, status=404)

    # بررسی دسترسی
    user = request.user
    has_access = False
    access_level = None

    if user.is_superuser:
        has_access = True
        access_level = 'full'
    else:
        access_entries = CredentialAccess.objects.filter(
            credential=credential
        ).filter(
            models_q_user_or_group(user)
        )
        if access_entries.exists():
            has_access = True
            access_level = access_entries.first().access_level

    if not has_access:
        # لاگ تلاش دسترسی غیرمجاز
        CredentialLog.objects.create(
            credential=credential,
            user=user,
            access_type='view',
            ip_address=_get_client_ip(request),
            details='تلاش دسترسی غیرمجاز به رمز عبور',
        )
        return JsonResponse({'error': 'دسترسی ندارید'}, status=403)

    # لاگ دسترسی موفق
    password = credential.password
    CredentialLog.objects.create(
        credential=credential,
        user=user,
        access_type='copy_password' if access_level in ('copy', 'edit', 'full') else 'view',
        ip_address=_get_client_ip(request),
    )

    return JsonResponse({
        'password': password,
        'access_level': access_level,
        'can_copy': access_level in ('copy', 'edit', 'full'),
    })


@staff_member_required
@require_POST
def copy_password(request, credential_id):
    """API برای کپی رمز عبور"""
    try:
        credential = Credential.objects.get(pk=credential_id)
    except Credential.DoesNotExist:
        return JsonResponse({'error': 'یافت نشد'}, status=404)

    user = request.user
    has_access = False

    if user.is_superuser:
        has_access = True
    else:
        has_access = CredentialAccess.objects.filter(
            credential=credential
        ).filter(
            models_q_user_or_group(user)
        ).filter(
            access_level__in=['copy', 'edit', 'full']
        ).exists()

    if not has_access:
        return JsonResponse({'error': 'دسترسی کپی ندارید'}, status=403)

    # لاگ کپی
    CredentialLog.objects.create(
        credential=credential,
        user=user,
        access_type='copy_password',
        ip_address=_get_client_ip(request),
    )

    return JsonResponse({'password': credential.password})


def models_q_user_or_group(user):
    """Q object برای فیلتر دسترسی بر اساس کاربر یا گروه"""
    from django.db.models import Q
    return Q(user=user) | Q(group__in=user.groups.all())


def _get_client_ip(request):
    """دریافت IP کلاینت"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')
