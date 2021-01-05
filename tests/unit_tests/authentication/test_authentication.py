import pytest
import responses # https://github.com/getsentry/responses
import time

from datacrunch.exceptions import APIException
from datacrunch.authentication.authentication import AuthenticationService

INVALID_REQUEST = 'invalid_request'
INVALID_REQUEST_MESSAGE = 'Your existence is invalid'

BASE_URL = "https://api-testing.datacrunch.io/v1"
CLIENT_ID = "0123456789xyz"
CLIENT_SECRET = 'zyx987654321'

ACCESS_TOKEN = 'access'
REFRESH_TOKEN = 'refresh'
SCOPE = 'fullAccess'
TOKEN_TYPE = 'Bearer'
EXPIRES_IN = 3600

class TestAuthenticationService:

    @pytest.fixture
    def authentication_service(self):
        return AuthenticationService(CLIENT_ID, CLIENT_SECRET, BASE_URL)

    @pytest.fixture
    def endpoint(self, http_client):
        return http_client._base_url + "/oauth2/token"

    def test_authenticate_successful(self, authentication_service, endpoint):
        # arrange - add response mock
        responses.add(
            responses.POST,
            endpoint,
            json={
                'access_token': ACCESS_TOKEN,
                'refresh_token': REFRESH_TOKEN,
                'scope': SCOPE,
                'token_type': TOKEN_TYPE,
                'expires_in': EXPIRES_IN
            },
            status=200
        )

        # act
        auth_data = authentication_service.authenticate()

        # assert
        assert type(auth_data) == dict
        assert authentication_service._access_token == ACCESS_TOKEN
        assert authentication_service._refresh_token == REFRESH_TOKEN
        assert authentication_service._scope == SCOPE
        assert authentication_service._token_type == TOKEN_TYPE
        assert authentication_service._expires_at != None
        assert responses.assert_call_count(endpoint, 1) is True

    def test_authenticate_failed(self, authentication_service, endpoint):
        # arrange - add response mock
        responses.add(
            responses.POST,
            endpoint,
            json={"code": INVALID_REQUEST, "message": INVALID_REQUEST_MESSAGE},
            status=400
        )

        # act
        with pytest.raises(APIException) as excinfo:
            authentication_service.authenticate()

        x = responses.calls[0].request

        # assert
        assert excinfo.value.code == INVALID_REQUEST
        assert excinfo.value.message == INVALID_REQUEST_MESSAGE
        assert responses.assert_call_count(endpoint, 1) is True
        assert responses.calls[0].request.body == f'grant_type=client_credentials&client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}'

    def test_refresh_successful(self, authentication_service, endpoint):
        responses.add(
            responses.POST,
            endpoint,
            json={
                'access_token': ACCESS_TOKEN,
                'refresh_token': REFRESH_TOKEN,
                'scope': SCOPE,
                'token_type': TOKEN_TYPE,
                'expires_in': EXPIRES_IN
            },
            status=200
        )

        # act
        authentication_service.authenticate() # authenticate first
        auth_data = authentication_service.refresh() # refresh

        # assert
        assert type(auth_data) == dict
        assert authentication_service._access_token == ACCESS_TOKEN
        assert authentication_service._refresh_token == REFRESH_TOKEN
        assert authentication_service._scope == SCOPE
        assert authentication_service._token_type == TOKEN_TYPE
        assert authentication_service._expires_at != None
        assert responses.calls[0].request.body == f'grant_type=client_credentials&client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}'
        assert responses.calls[1].request.body == f'grant_type=refresh_token&refresh_token={REFRESH_TOKEN}'
        assert responses.assert_call_count(endpoint, 2) is True

    def test_refresh_failed(self, authentication_service, endpoint):
        # arrange - add responses mock
        # first response for authentication - ok
        responses.add(
            responses.POST,
            endpoint,
            json={
                'access_token': ACCESS_TOKEN,
                'refresh_token': REFRESH_TOKEN,
                'scope': SCOPE,
                'token_type': TOKEN_TYPE,
                'expires_in': EXPIRES_IN
            },
            status=200
        )

        # second response for the refresh - failed
        responses.add(
            responses.POST,
            endpoint,
            json={"code": INVALID_REQUEST, "message": INVALID_REQUEST_MESSAGE},
            status=400
        )

        # act
        authentication_service.authenticate() # authenticate first

        with pytest.raises(APIException) as excinfo:
            authentication_service.refresh()

        # assert
        assert excinfo.value.code == INVALID_REQUEST
        assert excinfo.value.message == INVALID_REQUEST_MESSAGE
        assert responses.assert_call_count(endpoint, 2) is True
        assert responses.calls[0].request.body == f'grant_type=client_credentials&client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}'
        assert responses.calls[1].request.body == f'grant_type=refresh_token&refresh_token={REFRESH_TOKEN}'

    def test_is_expired(self, authentication_service, endpoint):
        # arrange
        current_time = time.time()
        future_time = current_time + 3600

        # act
        authentication_service._expires_at = current_time # set the expired_at as current time
        is_expired_current = authentication_service.is_expired()

        authentication_service._expires_at = future_time # set the expired_at as future time
        is_expired_future = authentication_service.is_expired()

        # assert
        assert is_expired_current == True
        assert is_expired_future == False