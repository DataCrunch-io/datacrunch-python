import requests
import time

from datacrunch.http_client.http_client import handle_error

TOKEN_ENDPOINT = '/oauth2/token'

CLIENT_CREDENTIALS = 'client_credentials'
REFRESH_TOKEN = 'refresh_token'


class AuthenticationService:
    """A service for client authentication"""

    def __init__(self, client_id: str, client_secret: str, base_url: str) -> None:
        self._base_url = base_url
        self._client_id = client_id
        self._client_secret = client_secret

    def authenticate(self) -> dict:
        """Authenticate the client and store the access & refresh tokens

        returns an authentication data dictionary with the following schema:
        {
            "access_token": token str,
            "refresh_token": token str,
            "scope": scope str,
            "token_type": token type str,
            "expires_in": duration until expires in seconds
        }

        :return: authentication data (tokens, scope, token type, expires in)
        :rtype: dict
        """
        url = self._base_url + TOKEN_ENDPOINT
        payload = {
            "grant_type": CLIENT_CREDENTIALS,
            "client_id": self._client_id,
            "client_secret": self._client_secret
        }

        response = requests.post(
            url, json=payload, headers=self._generate_headers())
        handle_error(response)

        auth_data = response.json()

        self._access_token = auth_data['access_token']
        self._refresh_token = auth_data['refresh_token']
        self._scope = auth_data['scope']
        self._token_type = auth_data['token_type']
        self._expires_at = time.time() + auth_data['expires_in']

        return auth_data

    def refresh(self) -> dict:
        """Authenticate the client using the refresh token - refresh the access token.

        updates the object's tokens, and:
        returns an authentication data dictionary with the following schema:
        {
            "access_token": token str,
            "refresh_token": token str,
            "scope": scope str,
            "token_type": token type str,
            "expires_in": duration until expires in seconds
        }

        :return: authentication data (tokens, scope, token type, expires in)
        :rtype: dict
        """
        url = self._base_url + TOKEN_ENDPOINT

        payload = {
            "grant_type": REFRESH_TOKEN,
            "refresh_token": self._refresh_token
        }

        response = requests.post(
            url, json=payload, headers=self._generate_headers())
        handle_error(response)

        auth_data = response.json()

        self._access_token = auth_data['access_token']
        self._refresh_token = auth_data['refresh_token']
        self._scope = auth_data['scope']
        self._token_type = auth_data['token_type']
        self._expires_at = time.time() + auth_data['expires_in']

        return auth_data

    def _generate_headers(self):
        # get the first 10 chars of the client id
        client_id_truncated = self._client_id[:10]
        headers = {
            'User-Agent': 'datacrunch-python-' + client_id_truncated
        }
        return headers

    def is_expired(self) -> bool:
        """Returns true if the access token is expired.

        :return: True if the access token is expired, otherwise False.
        :rtype: bool
        """
        return time.time() > self._expires_at
