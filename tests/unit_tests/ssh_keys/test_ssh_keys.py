import pytest
import responses # https://github.com/getsentry/responses

from datacrunch.exceptions import APIException
from datacrunch.ssh_keys.ssh_keys import SSHKeysService, SSHKey

INVALID_REQUEST = 'invalid_request'
INVALID_REQUEST_MESSAGE = 'Your existence is invalid'

KEY_ID = '01cf5dc1-a5d2-4972-ae4e-d429115d055b'
KEY_NAME = 'key to your heart'
KEY_VALUE = 'asdf'

KEY_ID_2 = '12345dc1-a5d2-4972-ae4e-d429115d055b'

PAYLOAD = [
    {
        'id': KEY_ID,
        'name': KEY_NAME,
        'key': KEY_VALUE
    }
]


class TestSSHKeys:

    @pytest.fixture
    def ssh_key_service(self, http_client):
        return SSHKeysService(http_client)

    @pytest.fixture
    def endpoint(self, http_client):
        return http_client._base_url + "/sshkeys"

    def test_get_keys(self, ssh_key_service, endpoint):
        # arrange - add response mock
        responses.add(
            responses.GET,
            endpoint,
            json=PAYLOAD,
            status=200
        )

        # act
        keys = ssh_key_service.get()
        
        # assert
        assert type(keys) == list
        assert len(keys) == 1
        assert type(keys[0]) == SSHKey
        assert keys[0].id == KEY_ID
        assert keys[0].name == KEY_NAME
        assert keys[0].public_key == KEY_VALUE
        assert responses.assert_call_count(endpoint, 1) is True

    def test_get_key_by_id_successful(self, ssh_key_service, endpoint):
        # arrange - add response mock
        url = endpoint + '/' + KEY_ID
        responses.add(
            responses.GET,
            url,
            json=PAYLOAD,
            status=200
        )

        # act
        key = ssh_key_service.get_by_id(KEY_ID)
        
        # assert
        assert type(key) == SSHKey
        assert key.id == KEY_ID
        assert key.name == KEY_NAME
        assert key.public_key == KEY_VALUE
        assert responses.assert_call_count(url, 1) is True

    def test_get_key_by_id_failed(self, ssh_key_service, endpoint):
        # arrange - add response mock
        url = endpoint + '/x'
        responses.add(
            responses.GET,
            url,
            json={"code": INVALID_REQUEST, "message": INVALID_REQUEST_MESSAGE},
            status=400
        )

        # act
        with pytest.raises(APIException) as excinfo:
            ssh_key_service.get_by_id('x')

        # assert
        assert excinfo.value.code == INVALID_REQUEST
        assert excinfo.value.message == INVALID_REQUEST_MESSAGE
        assert responses.assert_call_count(url, 1) is True

    def test_create_key_successful(self, ssh_key_service, endpoint):
        # arrange - add response mock
        responses.add(
            responses.POST,
            endpoint,
            body=KEY_ID,
            status=201
        )

        # act
        key = ssh_key_service.create(KEY_NAME, KEY_VALUE)
        
        # assert
        assert type(key) == SSHKey
        assert type(key.id) == str
        assert key.id == KEY_ID 
        assert responses.assert_call_count(endpoint, 1) is True

    def test_create_key_failed(self, ssh_key_service, endpoint):
        # arrange - add response mock
        responses.add(
            responses.POST,
            endpoint,
            json={"code": INVALID_REQUEST, "message": INVALID_REQUEST_MESSAGE},
            status=400
        )

        # act
        with pytest.raises(APIException) as excinfo:
            ssh_key_service.create(KEY_NAME, KEY_VALUE)

        # assert
        assert excinfo.value.code == INVALID_REQUEST
        assert excinfo.value.message == INVALID_REQUEST_MESSAGE
        assert responses.assert_call_count(endpoint, 1) is True

    def test_delete_keys_successful(self, ssh_key_service, endpoint):
        # arrange - add response mock
        responses.add(
            responses.DELETE,
            endpoint,
            status=200
        )

        # act
        result = ssh_key_service.delete([KEY_ID, KEY_ID_2])

        # assert
        assert result is None
        assert responses.assert_call_count(endpoint, 1) is True
        

    def test_delete_keys_failed(self, ssh_key_service, endpoint):
        # arrange - add response mock
        responses.add(
            responses.DELETE,
            endpoint,
            json={"code": INVALID_REQUEST, "message": INVALID_REQUEST_MESSAGE},
            status=400
        )

        # act
        with pytest.raises(APIException) as excinfo:
            ssh_key_service.delete(['x'])

        # assert
        assert excinfo.value.code == INVALID_REQUEST
        assert excinfo.value.message == INVALID_REQUEST_MESSAGE
        assert responses.assert_call_count(endpoint, 1) is True

    def test_delete_key_by_id_successful(self, ssh_key_service, endpoint):
        # arrange - add response mock
        url = endpoint + '/' + KEY_ID
        responses.add(
            responses.DELETE,
            url,
            status=200
        )

        # act
        result = ssh_key_service.delete_by_id(KEY_ID)

        # assert
        assert result == None
        assert responses.assert_call_count(url, 1) is True

    def test_delete_key_by_id_failed(self, ssh_key_service, endpoint):
        # arrange - add response mock
        url = endpoint + '/x'
        responses.add(
            responses.DELETE,
            url,
            json={"code": INVALID_REQUEST, "message": INVALID_REQUEST_MESSAGE},
            status=400
        )

        # act
        with pytest.raises(APIException) as excinfo:
            ssh_key_service.delete_by_id('x')

        # assert
        assert excinfo.value.code == INVALID_REQUEST
        assert excinfo.value.message == INVALID_REQUEST_MESSAGE
        assert responses.assert_call_count(url, 1) is True