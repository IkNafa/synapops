from urllib.parse import urljoin
import requests

from .actions import Actions
from .settings import PLAYBOOKS_URI, HEALTH_URI, DEFAULT_TIMEOUT
from .exceptions import (
    AnsibleConnectionError,
    AnsibleRequestError,
)

class AnsibleClient:
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url.rstrip("/")
        self.playbooks_url = urljoin(self.base_url, PLAYBOOKS_URI)

        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        })

        self._test_connection()

    def _test_connection(self) -> None:
        try:
            self.session.get(
                urljoin(self.base_url, HEALTH_URI),
                timeout=5
            ).raise_for_status()
        except requests.RequestException as exc:
            raise AnsibleConnectionError from exc

    def _run_playbook(self, key: str, payload: dict) -> None:
        try:
            self.session.post(
                self.playbooks_url,
                params={"key": key},
                json=payload,
                timeout=DEFAULT_TIMEOUT,
            ).raise_for_status()
        except requests.RequestException as exc:
            raise AnsibleRequestError from exc

    def _set_service_state(self, service: str, state: str) -> None:
        if not service:
            raise AnsibleRequestError("Service name must be provided.")
        self._run_playbook(
            Actions.SYSTEM.SERVICE.value,
            {
                "service_name": service,
                "service_state": state,
            }
        )

    def start_service(self, service: str) -> None:
        self._set_service_state(service, "started")
    
    def stop_service(self, service: str) -> None:
        self._set_service_state(service, "stopped")
    
    def restart_service(self, service: str) -> None:
        self._set_service_state(service, "restarted")
