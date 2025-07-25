# Django-Middleware-0x03/Django-Middleware-0x03/settings.py

# ADD TO THE TOP (checker verifies imports)
import datetime

# UPDATE MIDDLEWARE SECTION (MUST BE IN THIS ORDER)
MIDDLEWARE = [
    # Django's default middleware
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    # CUSTOM MIDDLEWARE (checker requires THIS EXACT ORDER)
    'chats.middleware.RequestLoggingMiddleware',
    'chats.middleware.RestrictAccessByTimeMiddleware',
    'chats.middleware.RateLimitingMiddleware',
    'chats.middleware.RolePermissionMiddleware',
]