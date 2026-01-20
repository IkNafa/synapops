from .views import (
    start_environment_service, stop_environment_service, restart_environment_service
)
from django.urls import path

urlpatterns = [
    path('<int:pk>/start/', start_environment_service, {'action': 'start'} ,name='start-environment'),
    path('<int:pk>/stop/', stop_environment_service, {'action': 'stop'} ,name='stop-environment'),
    path('<int:pk>/restart/', restart_environment_service, {'action': 'restart'} ,name='restart-environment'),
]