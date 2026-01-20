from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse
from django.shortcuts import get_object_or_404

from apps.environments.services import get_ansible_client, EnvironmentError
from apps.base.services.ansible import AnsibleError
from apps.environments.models import Environment

from typing import Literal

ACTION_MAP = {
    "start": "start_service",
    "stop": "stop_service",
    "restart": "restart_service",
}

systemd_action_schema = {
    'methods': ['POST'],
    'request': None,
    'tags': ['Environments - Systemd'],
    'responses': {
        200: OpenApiResponse(description="Action performed successfully"),
        400: OpenApiResponse(description="Invalid action or bad request"),
        502: OpenApiResponse(description="Ansible service error"),
    },
}

@extend_schema(summary="Start", operation_id="start_environment_service", **systemd_action_schema)
@api_view(['POST'])
def start_environment_service(request, pk):
    return _environment_systemd_action(request, pk, action='start')

@extend_schema(summary="Stop", operation_id="stop_environment_service", **systemd_action_schema)
@api_view(['POST'])
def stop_environment_service(request, pk):
    return _environment_systemd_action(request, pk, action='stop')

@extend_schema(summary="Restart", operation_id="restart_environment_service", **systemd_action_schema)
@api_view(['POST'])
def restart_environment_service(request, pk):
    return _environment_systemd_action(request, pk, action='restart')


def _environment_systemd_action(request, pk: int, action: Literal["start", "stop", "restart"]):
    environment = get_object_or_404(Environment, pk=pk)
    try:
        ansible_client = get_ansible_client(environment)
        action_method = ACTION_MAP.get(action)
        service_name = environment.systemd_service_name
        if not action_method:
            return Response({'error': 'Invalid action'}, status=400)

        method = getattr(ansible_client, action_method)
        if not callable(method):
            return Response({'error': 'Action method not callable'}, status=400)
        method(service_name)
        return Response({'status': 'success'})
    except EnvironmentError as e:
        return Response({"error": str(e)}, status=400)
    except AnsibleError as e:
        return Response({"error": str(e)}, status=502)