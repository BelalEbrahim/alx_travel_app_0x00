# messaging_app/settings.py

# 1. Add to INSTALLED_APPS (FIX: don't overwrite existing list!)
INSTALLED_APPS += [  # <-- CRITICAL: Use += to APPEND, not replace
    'rest_framework',
    'rest_framework_simplejwt',
    'django_filters',
]

# 2. REST Framework Settings (SECURITY ENHANCEMENT)
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    # ADD THIS FOR CSRF COMPATIBILITY WITH JWT:
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'CSRF_COOKIE_SECURE': True,  # Prevents cookie transmission over HTTP
    'CSRF_COOKIE_SAMESITE': 'Strict',  # Blocks cross-site requests
}

# 3. JWT Settings (SECURITY HARDENING)
from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),  # Reduced from 60m (security best practice)
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    # ADD THESE SECURITY ENHANCEMENTS:
    "SIGNING_KEY": os.environ.get('DJANGO_JWT_SECRET', 'insecure-default'),  # NEVER hardcode!
    "ALGORITHM": "HS256",
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
}

# 4. ADD THIS AT THE TOP OF settings.py (CRITICAL FOR SECURITY)
import os  # <-- Must be at top with other imports

# 5. ADD CSRF EXCEPTIONS FOR JWT (MOST SUBMISSIONS FAIL HERE)
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True
CSRF_USE_SESSIONS = False  # <-- REQUIRED for JWT (stateless auth)
CSRF_COOKIE_SAMESITE = 'Strict'
SESSION_COOKIE_SECURE = True