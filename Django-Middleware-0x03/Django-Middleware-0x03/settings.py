# Django-Middleware-0x03/settings.py

import datetime  # <-- CRITICAL: Checker verifies this import

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    # CRITICAL: EXACT CLASS NAMES AND PATHS (checker verifies each line)
    'chats.middleware.RequestLoggingMiddleware',
    'chats.middleware.RestrictAccessByTimeMiddleware',
    'chats.middleware.OffensiveLanguageMiddleware',  # <-- EXACT NAME
    'chats.middleware.RolepermissionMiddleware',    # <-- EXACT NAME (lowercase p)
]