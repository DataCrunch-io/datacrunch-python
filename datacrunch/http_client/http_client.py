import requests
import json

from datacrunch.exceptions import APIException
from datacrunch.__version__ import VERSION


def handle_error(response: requests.Response) -> None:
    """checks for the response status code and raises an exception if it's 400 or higher.

    :param response: the API call response
    :raises APIException: an api exception with message and error type code
    """
    if not response.ok:
        data = json.loads(response.text)
        code = data['code'] if 'code' in data else None
        message = data['message'] if 'message' in data else None
        raise APIException(code, message)


class HTTPClient:
    """An http client, a wrapper for the requests library.

    For each request, it adds the authentication header with an access token.
    If the access token is expired it refreshes it before calling the specified API endpoint.
    Also checks the response status code and raises an exception if needed.
    """

    def __init__(self, auth_service, base_url: str) -> None:
        self._version = VERSION
        self._base_url = base_url
        self._auth_service = auth_service
        self._auth_service.authenticate()

    def post(self, url: str, json: dict = None, **kwargs) -> requests.Response:
        """Sends a POST request.

        A wrapper for the requests.post method.

        Builds the url, uses custom headers, refresh tokens if needed.

        :param url: relative url of the API endpoint
        :type url: str
        :param json: A JSON serializable Python object to send in the body of the Request, defaults to None
        :type json: dict, optional

        :raises APIException: an api exception with message and error type code

        :return: Response object
        :rtype: requests.Response
        """
        url = self._add_base_url(url)
        headers = self._generate_headers()

        self._refresh_token_if_expired()

        response = requests.post(url, json=json, headers=headers, **kwargs)
        handle_error(response)

        return response

    def put(self, url: str, json: dict = None, **kwargs) -> requests.Response:
        """Sends a PUT request.

        A wrapper for the requests.put method.

        Builds the url, uses custom headers, refresh tokens if needed.

        :param url: relative url of the API endpoint
        :type url: str
        :param json: A JSON serializable Python object to send in the body of the Request, defaults to None
        :type json: dict, optional

        :raises APIException: an api exception with message and error type code

        :return: Response object
        :rtype: requests.Response
        """
        url = self._add_base_url(url)
        headers = self._generate_headers()

        self._refresh_token_if_expired()

        response = requests.put(url, json=json, headers=headers, **kwargs)
        handle_error(response)

        return response

    def get(self, url: str, params: dict = None, **kwargs) -> requests.Response:
        """Sends a GET request.

        A wrapper for the requests.get method.

        Builds the url, uses custom headers, refresh tokens if needed.

        :param url: relative url of the API endpoint
        :type url: str
        :param params: Dictionary, list of tuples or bytes to send in the query string for the Request. defaults to None
        :type params: dict, optional

        :raises APIException: an api exception with message and error type code

        :return: Response object
        :rtype: requests.Response
        """
        url = self._add_base_url(url)
        headers = self._generate_headers()

        self._refresh_token_if_expired()

        response = requests.get(url, params=params, headers=headers, **kwargs)
        handle_error(response)

        return response

    def delete(self, url: str, json: dict = None, **kwargs) -> requests.Response:
        """Sends a DELETE request.

        A wrapper for the requests.delete method.

        Builds the url, uses custom headers, refresh tokens if needed.

        :param url: relative url of the API endpoint
        :type url: str
        :param json: A JSON serializable Python object to send in the body of the Request, defaults to None
        :type json: dict, optional

        :raises APIException: an api exception with message and error type code

        :return: Response object
        :rtype: requests.Response
        """
        url = self._add_base_url(url)
        headers = self._generate_headers()

        self._refresh_token_if_expired()

        response = requests.delete(url, headers=headers, json=json, **kwargs)
        handle_error(response)

        return response

    def _refresh_token_if_expired(self) -> None:
        """refreshes the access token if it expired.

        Uses the refresh token to refresh, and if the refresh token is also expired, uses the client credentials.

        :raises APIException: an api exception with message and error type code
        """
        if(self._auth_service.is_expired()):
            # to to refresh. if refresh token has expired, reauthenticate
            try:
                self._auth_service.refresh()
            except Exception:
                self._auth_service.authenticate()

    def _generate_headers(self) -> dict:
        """generate the default headers for every request

        :return: dict with request headers
        :rtype: dict
        """
        headers = {
            'Authorization': self._generate_bearer_header(),
            'User-Agent': self._generate_user_agent(),
            'Content-Type': 'application/json'
        }
        return headers

    def _generate_bearer_header(self) -> str:
        """generate the authorization header Bearer string

        :return: Authorization header Bearer string
        :rtype: str
        """
        return f'Bearer {self._auth_service._access_token}'

    def _generate_user_agent(self) -> str:
        """generate the user agent string.

        :return: user agent string
        :rtype: str
        """
        client_id_truncated = self._auth_service._client_id[:
                                                            10]  # get the first 10 chars of the client id

        return f'datacrunch-python-v{self._version}-{client_id_truncated}'

    def _add_base_url(self, url: str) -> str:
        """Adds the base url to the relative url

        example:
        if the relative url is '/balance'
        and the base url is 'https://api.datacrunch.io/v1'
        then this method will return 'https://api.datacrunch.io/v1/balance'

        :param url: a relative url path
        :type url: str
        :return: the full url path
        :rtype: str
        """
        return self._base_url + url
