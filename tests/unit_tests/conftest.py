import pytest
from unittest.mock import Mock
from datacrunch.http_client.http_client import HTTPClient


BASE_URL = "https://api-testing.datacrunch.io/v1"
ACCESS_TOKEN = "test-token"
CLIENT_ID = "0123456789xyz"


@pytest.fixture
def http_client():
    auth_service = Mock()
    auth_service._access_token = ACCESS_TOKEN
    auth_service.is_expired = Mock(return_value=True)
    auth_service.refresh = Mock(return_value=None)
    auth_service._client_id = CLIENT_ID

    return HTTPClient(auth_service, BASE_URL)
