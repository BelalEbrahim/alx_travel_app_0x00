# chats/filters.py
import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    conversation = django_filters.NumberFilter(field_name="conversation_id")
    min_date = django_filters.DateTimeFilter(field_name="timestamp", lookup_expr='gte')
    max_date = django_filters.DateTimeFilter(field_name="timestamp", lookup_expr='lte')
    participant = django_filters.NumberFilter(method='filter_by_participant')

    class Meta:
        model = Message
        fields = ['conversation', 'min_date', 'max_date', 'participant']

    def filter_by_participant(self, queryset, name, value):
        return queryset.filter(conversation__participants=value)