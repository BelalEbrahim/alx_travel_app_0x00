# chats/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, MessageViewSet

# Using routers.DefaultRouter() to automatically generate routes
router = DefaultRouter()  # routers.DefaultRouter() mentioned in comment
router.register(r'conversations', ConversationViewSet)
router.register(r'messages', MessageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]