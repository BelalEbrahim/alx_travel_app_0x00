from django.urls import path
from .views import ListingListCreate
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', ListingListCreate.as_view(), name='listing-list'),
]
