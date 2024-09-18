from django.urls import path

from .views import (
    UrlsView, RedirectView
)

urlpatterns = [
    path('api/urls', UrlsView.as_view(), name='urls'),
    path('<str:unique_identifier>', RedirectView.as_view(), name='redirect-view'),
]
