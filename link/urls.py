from django.urls import path

from .views import (
    UrlsView, RedirectView,
    UrlView, DisableUrlView, EnableUrlView,
)

urlpatterns = [
    path('api/urls', UrlsView.as_view(), name='urls'),
    path('<str:unique_identifier>', RedirectView.as_view(), name='redirect_view'),
    path('api/urls/<int:pk>', UrlView.as_view(), name='url'),
    path('api/urls/<int:pk>/disable', DisableUrlView.as_view(), name='disable_url'),
    path('api/urls/<int:pk>/enable', EnableUrlView.as_view(), name='enable_url'),

]
