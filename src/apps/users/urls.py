from django.urls import path

from .views import (
    github_connect,
    github_installation_callback,
    github_webhook
)

urlpatterns = [
    path('github/connect/', github_connect, name='github-connect'),
    path('github/callback/', github_installation_callback, name='github-callback'),
    path('github/webhook/', github_webhook, name='github-webhook'),
]