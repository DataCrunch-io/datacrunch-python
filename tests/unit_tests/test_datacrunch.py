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
    sys.modules.pop('verda.datacrunch', None)


def test_datacrunch_client_deprecation():
    from verda import DataCrunchClient

    responses.add(responses.POST, BASE_URL + '/oauth2/token', json=response_json, status=200)

    with pytest.warns(DeprecationWarning, match='DataCrunchClient is deprecated'):
        client = DataCrunchClient('XXXXXXXXXXXXXX', 'XXXXXXXXXXXXXX', BASE_URL)

    assert client.constants.base_url == BASE_URL


@pytest.mark.filterwarnings('ignore:DataCrunchClient is deprecated')
def test_datacrunch_module_deprecation():
    responses.add(responses.POST, BASE_URL + '/oauth2/token', json=response_json, status=200)

    with pytest.warns(DeprecationWarning, match='datacrunch.datacrunch is deprecated'):
        from verda.datacrunch import DataCrunchClient

    client = DataCrunchClient('XXXXXXXXXXXXXX', 'XXXXXXXXXXXXXX', BASE_URL)
    assert client.constants.base_url == BASE_URL


def test_datacrunch_constants_module():
    # Test that old re-exports in datacrunch.datacrunch (sub)module still work, but warn

    with pytest.warns(DeprecationWarning, match='datacrunch.datacrunch is deprecated'):
        from verda.datacrunch import Constants

    constants = Constants('url', 'v1')

    assert constants.base_url == 'url'
    assert constants.version == 'v1'
