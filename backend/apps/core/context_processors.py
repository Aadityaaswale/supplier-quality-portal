def global_context(request):
    role = None
    if request.user.is_authenticated:
        if hasattr(request.user, 'profile'):
            role = request.user.profile.role
        elif request.user.is_superuser:
            role = 'ADMIN'
        else:
            role = 'REVIEWER'

    return {
        'APP_NAME': 'Supplier Quality Review Portal',
        'STUDENT_NAME': 'AADITYA ASWALE',
        'STUDENT_ID': '23102B0044',
        'CURRENT_USER_ROLE': role,
        'IS_ADMIN': role == 'ADMIN',
        'IS_QUALITY_MANAGER': role in ['ADMIN', 'QUALITY_MANAGER'],
        'IS_REVIEWER': role in ['ADMIN', 'QUALITY_MANAGER', 'REVIEWER'],
    }
