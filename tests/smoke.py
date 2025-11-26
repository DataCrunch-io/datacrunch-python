import responses

from verda import VerdaClient

BASE_URL = 'https://example.com'


@responses.activate()
def main():
    responses.add(
        responses.POST,
        f'{BASE_URL}/oauth2/token',
        json={
            'access_token': 'dummy',
            'token_type': 'Bearer',
            'refresh_token': 'dummy',
            'scope': 'fullAccess',
            'expires_in': 3600,
        },
        status=200,
    )

    client = VerdaClient('id', 'secret', BASE_URL)
    assert client.constants.base_url == BASE_URL


if __name__ == '__main__':
    main()
