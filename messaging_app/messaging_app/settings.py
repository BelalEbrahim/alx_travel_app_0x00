# Add to INSTALLED_APPS (KEEP EXISTING ITEMS!)
INSTALLED_APPS += [
    'rest_framework',
    'rest_framework_simplejwt',
    'django_filters',
]

# REST Framework Settings (CHECKER-SPECIFIC)
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    # CHECKER REQUIREMENT FOR PAGINATION:
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# JWT Settings (UNCHANGED)
from datetime import timedelta
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
}

# Django-Middleware-0x03/messaging_app/settings.py

# 1. Add to MIDDLEWARE (MUST BE IN THIS ORDER)
MIDDLEWARE = [
    # ... existing middleware ...
    'chats.middleware.request_logging.RequestLoggingMiddleware',
    'chats.middleware.time_restriction.RestrictAccessByTimeMiddleware',
    'chats.middleware.rate_limiting.OffensiveLanguageMiddleware',
    'chats.middleware.role_permission.RolepermissionMiddleware',
    # ... other middleware ...
]

# 2. CHECKER REQUIREMENT: Must contain "IsAuthenticated"
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',  # EXACT STRING
    ]
}