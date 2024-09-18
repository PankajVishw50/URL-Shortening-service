from django.urls import path

from .views import (
    UrlsView, RedirectView,
    UrlView,
)

urlpatterns = [
    path('api/urls', UrlsView.as_view(), name='urls'),
    path('<str:unique_identifier>', RedirectView.as_view(), name='redirect-view'),
    path('api/urls/<int:pk>', UrlView.as_view(), name='url'),
]
