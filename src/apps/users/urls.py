from django.urls import path

from .views import GitHubConnectionAPIView, GitHubInstallationCallbackAPIView, GitHubWebhookAPIView

urlpatterns = [
    path('github/connect/', GitHubConnectionAPIView.as_view(), name='github-connect'),
    path('github/callback/', GitHubInstallationCallbackAPIView.as_view(), name='github-callback'),
    path('github/webhook/', GitHubWebhookAPIView.as_view(), name='github-webhook'),
]