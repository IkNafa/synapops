from requests import Response
from rest_framework.decorators import api_view
from django.core import signing
from django.conf import settings

from drf_spectacular.utils import extend_schema, OpenApiResponse

from apps.users.services import GitHubService
from apps.users.models import GitHubOrganization

from django.shortcuts import redirect

ORGANIZATION_ID = 1

@extend_schema(
    summary="Installation Connect",
    tags=["Integrations - GitHub"],
    responses={
        302: OpenApiResponse(description="Redirect to GitHub installation page"),
    },
)
@api_view(['GET'])
def github_connect(request):
    next_path = request.query_params.get('next', '/')
    payload = {
        'organization_id': ORGANIZATION_ID,
        'next': next_path
    }
    state = signing.dumps(payload, salt='github-install', compress=True)
    github_connect_url = f"https://github.com/apps/{settings.GITHUB_APP_NAME}/installations/new?state={state}"

    return redirect(github_connect_url)

@extend_schema(
    summary="Installation Callback",
    tags=["Integrations - GitHub"],
    responses={
        302: OpenApiResponse(description="Redirect to frontend with success or error message"),
    },
)
@api_view(['GET'])
def github_installation_callback(request):
    state = request.query_params.get('state')
    code = request.query_params.get('installation_id')
    action = request.query_params.get('setup_action')

    next_path = None
    redirect_url = None

    try:
        payload = signing.loads(state, salt='github-install', max_age=300)
        organization_id = payload.get('organization_id')
        next_path = payload.get('next')
    except signing.BadSignature:
        if next_path:
            redirect_url = f"{settings.FRONTEND_URL}{next_path}?error=invalid_state"
        return redirect(redirect_url or f'{settings.FRONTEND_URL}/error?message=Invalid+state+parameter')

    github = GitHubService(installation_id=code, app_id=settings.GITHUB_APP_ID, private_key=settings.GITHUB_APP_PRIVATE_KEY)
    organization_info = github.get_installation_info()

    GitHubOrganization.objects.update_or_create(
        github_org_id=organization_info.get("id"),
        defaults={
            "organization_id": organization_id,
            "login": organization_info.get("login"),
            "installation_id": code,
        }
    )

    if next_path:
        redirect_url = f"{settings.FRONTEND_URL}{next_path}?success=1"
    return redirect(redirect_url or f'{settings.FRONTEND_URL}/success?message=GitHub+installation+successful')
    
@extend_schema(
    summary="Webhook",
    request=None,
    tags=["Integrations - GitHub"],
    responses={
        200: OpenApiResponse(description="Webhook received successfully"),
    },
)
@api_view(['POST'])
def github_webhook(request):
    event_type = request.headers.get('X-GitHub-Event')
    payload = request.data

    print(f"Received GitHub webhook event: {event_type}")
    print(payload)

    return Response(status=200)


    