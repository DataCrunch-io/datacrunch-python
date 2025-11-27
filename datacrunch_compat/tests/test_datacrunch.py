import sys

import pytest
import responses  # https://github.com/getsentry/responses

BASE_URL = 'https://api.example.com/v1'

response_json = {
    'access_token': 'SECRET',
    'token_type': 'Bearer',
    'expires_in': 3600,
    'refresh_token': 'SECRET',
    'scope': 'fullAccess',
}


@pytest.fixture(autouse=True)
def reset_verda_datacrunch():
    # Ensure this module gets freshly imported in each test. Python normally caches imports,
    # which prevents module-level DeprecationWarnings from firing more than once.
    sys.modules.pop('datacrunch.datacrunch', None)
    sys.modules.pop('datacrunch', None)


def test_datacrunch_client_deprecation():
    with pytest.warns(DeprecationWarning, match='datacrunch is deprecated'):
        from datacrunch import DataCrunchClient

    responses.add(responses.POST, BASE_URL + '/oauth2/token', json=response_json, status=200)
    client = DataCrunchClient('XXXXXXXXXXXXXX', 'XXXXXXXXXXXXXX', BASE_URL)
    assert client.constants.base_url == BASE_URL


def test_datacrunch_module_deprecation():
    with pytest.warns(DeprecationWarning, match='datacrunch is deprecated'):
        from datacrunch.datacrunch import DataCrunchClient

    responses.add(responses.POST, BASE_URL + '/oauth2/token', json=response_json, status=200)
    client = DataCrunchClient('XXXXXXXXXXXXXX', 'XXXXXXXXXXXXXX', BASE_URL)
    assert client.constants.base_url == BASE_URL


def test_datacrunch_constants_module():
    # Test that old re-exports in datacrunch.datacrunch (sub)module still work, but warn

    with pytest.warns(DeprecationWarning, match='datacrunch is deprecated'):
        from datacrunch.datacrunch import Constants

    constants = Constants('url', 'v1')

    assert constants.base_url == 'url'
    assert constants.version == 'v1'


def test_datacrunch_constants_submodule():
    # Test that old re-exports in datacrunch.constants still work

    with pytest.warns(DeprecationWarning, match='datacrunch is deprecated'):
        from datacrunch.constants import Locations

    assert Locations.FIN_03 == 'FIN-03'


def test_datacrunch_inference_submodule():
    # Test that old re-exports in datacrunch.InferenceClient.* still work

    with pytest.warns(DeprecationWarning, match='datacrunch is deprecated'):
        from datacrunch.InferenceClient.inference_client import AsyncStatus

    assert AsyncStatus.Initialized == 'Initialized'
