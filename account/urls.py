from django.urls import path

from .views import (
    CSRFView,
    LoginView, SignUpView,
)

urlpatterns = [
    path('csrf', CSRFView.as_view(), name='csrf'),
    path('login', LoginView.as_view(), name='login'),
    path('signup', SignUpView.as_view(), name='signup'),
]
