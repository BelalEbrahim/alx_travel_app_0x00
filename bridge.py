Django-signals_orm-0x04/
├── messaging/
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py
│   ├── signals.py
│   ├── admin.py
│   ├── tests.py
│   └── views.py
├── messaging_app/
│   └── settings.py
└── chats/
    └── views.py

1. messaging/models.py

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Manager, Q

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.PROTECT, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.PROTECT, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    edited = models.BooleanField(default=False)
    parent_message = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    
    # Custom manager for unread messages
    objects = Manager()
    
    class UnreadMessagesManager(Manager):
        def for_user(self, user):
            return self.filter(receiver=user, read=False)
    
    unread = UnreadMessagesManager()
    
    def __str__(self):
        return f"Message {self.id} from {self.sender}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Notification for {self.user}"

class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"History for Message {self.message.id}"


2. messaging/signals.py

from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory
from django.contrib.auth.models import User

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:
        original = Message.objects.get(pk=instance.pk)
        if original.content != instance.content:
            MessageHistory.objects.create(
                message=instance,
                old_content=original.content
            )
            instance.edited = True

@receiver(pre_delete, sender=User)
def delete_user_data(sender, instance, **kwargs):
    # Delete related messages and notifications
    Message.objects.filter(Q(sender=instance) | Q(receiver=instance)).delete()
    Notification.objects.filter(user=instance).delete()

3. messaging/apps.py

from django.apps import AppConfig

class MessagingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'messaging'

    def ready(self):
        import messaging.signals

4. messaging/views.py

from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.shortcuts import render, get_object_or_404
from .models import Message

@vary_on_cookie
@cache_page(60)
def conversation_view(request, conversation_id):
    # Get root message and prefetch replies
    root_message = get_object_or_404(
        Message.objects.prefetch_related('replies'),
        id=conversation_id,
        parent_message__isnull=True
    )
    return render(request, 'conversation.html', {'root_message': root_message})

def delete_user(request):
    if request.method == 'POST':
        request.user.delete()
        # Add redirect/logout logic
    # Add confirmation template

5. messaging/admin.py

from django.contrib import admin
from .models import Message, Notification, MessageHistory

admin.site.register(Message)
admin.site.register(Notification)
admin.site.register(MessageHistory)

6. messaging_app/settings.py (partial)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

7. chats/views.py

from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.shortcuts import render
from messaging.models import Message

@vary_on_cookie
@cache_page(60)
def conversation_list(request):
    # Get conversations with optimization
    conversations = Message.objects.filter(
        parent_message__isnull=True
    ).select_related('sender', 'receiver').prefetch_related('replies')
    
    return render(request, 'conversations.html', {'conversations': conversations})

8. messaging/tests.py (sample tests)

from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification

class SignalTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user('user1')
        self.user2 = User.objects.create_user('user2')
    
    def test_notification_creation(self):
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Test message"
        )
        self.assertEqual(Notification.objects.count(), 1)
        notification = Notification.objects.first()
        self.assertEqual(notification.user, self.user2)
    
    def test_message_edit_log(self):
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Original content"
        )
        message.content = "Updated content"
        message.save()
        self.assertEqual(MessageHistory.objects.count(), 1)
        self.assertTrue(message.edited)



