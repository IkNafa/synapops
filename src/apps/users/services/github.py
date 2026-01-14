import requests
import time
import jwt

BASE_URL = 'https://api.github.com'

class GitHubService:
    def __init__(self, installation_id, app_id, private_key):
        self.installation_id = installation_id
        self.app_id = app_id
        self.private_key = private_key
        self._app_token = self._get_app_token()
        self._user_token = self._get_installation_access_token()

    def _get_app_token(self):
        now = int(time.time())

        payload = {
            "iat": now - 60,
            "exp": now + (10 * 60),
            "iss": self.app_id,
        }

        return jwt.encode(payload, self.private_key, algorithm="RS256")

    def _installation_headers(self):
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {self._app_token}",
        }
        return headers
    
    def _app_headers(self):
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {self._app_token}",
        }
        return headers

    def _get_installation_access_token(self):
        url = f"{BASE_URL}/app/installations/{self.installation_id}/access_tokens"
        headers = self._app_headers()
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data.get("token")
    
    def list_repositories(self):
        url = f"{BASE_URL}/app/installations/{self.installation_id}/repositories"
        headers = self._installation_headers()
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data.get("repositories", [])
    
    def get_installation_info(self):
        url = f"{BASE_URL}/app/installations/{self.installation_id}"
        headers = self._app_headers()
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json().get("account", {})
    
        