INSTALLED_APPS = [
    ...,
    'rest_framework',
    'chats',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    
}

AUTH_USER_MODEL = 'chats.User'  # Move this line outside of REST_FRAMEWORK
