from apps.base.services.ansible import AnsibleClient

from apps.environments.models import Environment

class EnvironmentError(Exception):
    pass

def get_ansible_client(environment: Environment) -> AnsibleClient:
    server = environment.server
    if not server or not server.agent_url or not server.agent_token:
        raise EnvironmentError("Server or agent details are missing.")
    
    return AnsibleClient(
        base_url=server.agent_url,
        token=server.agent_token
    )