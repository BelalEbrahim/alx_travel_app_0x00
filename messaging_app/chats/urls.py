# chats/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, MessageViewSet

# Explicitly create DefaultRouter instance
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet)
router.register(r'messages', MessageViewSet)

# Note: We are using DefaultRouter for routing, not NestedDefaultRouter
urlpatterns = [
    path('', include(router.urls)),
]