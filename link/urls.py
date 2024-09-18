from django.urls import path

from .views import (
    UrlsView, RedirectView,
    UrlView, DisableUrlView, EnableUrlView,
    VisitsView, VisitView, StatsView
)

urlpatterns = [
    path('api/urls', UrlsView.as_view(), name='urls'),
    path('<str:unique_identifier>', RedirectView.as_view(), name='redirect_view'),
    path('api/urls/<int:pk>', UrlView.as_view(), name='url'),
    path('api/urls/<int:pk>/disable', DisableUrlView.as_view(), name='disable_url'),
    path('api/urls/<int:pk>/enable', EnableUrlView.as_view(), name='enable_url'),
    path('api/urls/<int:pk>/visits', VisitsView.as_view(), name='visits'), 
    path('api/urls/<int:pk>/visits/<int:visit_pk>', VisitView.as_view(), name='visit'),
    path('api/urls/stats', StatsView.as_view(), name='stats'),

]
