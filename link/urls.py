from django.urls import path

from .views import (
    UrlsView,
)

urlpatterns = [
    path('urls', UrlsView.as_view(), name='urls'),
]
