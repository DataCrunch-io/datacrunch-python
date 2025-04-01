from dataclasses import dataclass
from dataclasses_json import dataclass_json, Undefined  # type: ignore
import requests
from requests.structures import CaseInsensitiveDict
from typing import Optional, Dict, Any, Union
from urllib.parse import urlparse


class InferenceClientError(Exception):
    """Base exception for InferenceClient errors."""
    pass


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class InferenceResponse:
    body: Any
    headers: CaseInsensitiveDict[str]
    status_code: int
    status_text: str


class InferenceClient:
    def __init__(self, inference_key: str, endpoint_base_url: str, timeout_seconds: int = 300) -> None:
        """
        Initialize the InferenceClient.

        Args:
            inference_key: The authentication key for the API
            endpoint_base_url: The base URL for the API
            timeout_seconds: Request timeout in seconds

        Raises:
            InferenceClientError: If the parameters are invalid
        """
        if not inference_key:
            raise InferenceClientError("inference_key cannot be empty")

        parsed_url = urlparse(endpoint_base_url)
        if not parsed_url.scheme or not parsed_url.netloc:
            raise InferenceClientError("endpoint_base_url must be a valid URL")

        self.inference_key = inference_key
        self.endpoint_base_url = endpoint_base_url.rstrip('/')
        self.timeout_seconds = timeout_seconds
        self._session = requests.Session()
        self._global_headers = {
            'Authorization': f'Bearer {inference_key}',
            'Content-Type': 'application/json'
        }

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._session.close()

    @property
    def global_headers(self) -> Dict[str, str]:
        """
        Get the current global headers that will be used for all requests.

        Returns:
            Dictionary of current global headers
        """
        return self._global_headers.copy()

    def set_global_header(self, key: str, value: str) -> None:
        """
        Set or update a global header that will be used for all requests.

        Args:
            key: Header name
            value: Header value
        """
        self._global_headers[key] = value

    def set_global_headers(self, headers: Dict[str, str]) -> None:
        """
        Set multiple global headers at once that will be used for all requests.

        Args:
            headers: Dictionary of headers to set globally
        """
        self._global_headers.update(headers)

    def remove_global_header(self, key: str) -> None:
        """
        Remove a global header.

        Args:
            key: Header name to remove from global headers
        """
        if key in self._global_headers:
            del self._global_headers[key]

    def _build_url(self, path: str) -> str:
        """Construct the full URL by joining the base URL with the path."""
        return f"{self.endpoint_base_url}/{path.lstrip('/')}"

    def _build_request_headers(self, request_headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """
        Build the final headers by merging global headers with request-specific headers.

        Args:
            request_headers: Optional headers specific to this request

        Returns:
            Merged headers dictionary
        """
        headers = self._global_headers.copy()
        if request_headers:
            headers.update(request_headers)
        return headers

    def _make_request(self, method: str, path: str, **kwargs) -> requests.Response:
        """
        Make an HTTP request with error handling.

        Args:
            method: HTTP method to use
            path: API endpoint path
            **kwargs: Additional arguments to pass to the request

        Returns:
            Response object from the request

        Raises:
            InferenceClientError: If the request fails
        """
        timeout = kwargs.pop('timeout_seconds', self.timeout_seconds)
        try:
            response = self._session.request(
                method=method,
                url=self._build_url(path),
                headers=self._build_request_headers(
                    kwargs.pop('headers', None)),
                timeout=timeout,
                **kwargs
            )
            response.raise_for_status()
            return response
        except requests.exceptions.Timeout:
            raise InferenceClientError(
                f"Request to {path} timed out after {timeout} seconds")
        except requests.exceptions.RequestException as e:
            raise InferenceClientError(f"Request to {path} failed: {str(e)}")

    def run_sync(self, data: Dict[str, Any], path: str = "", timeout_seconds: int = 60 * 5, headers: Optional[Dict[str, str]] = None):
        response = self.post(
            path, json=data, timeout_seconds=timeout_seconds, headers=headers)

        return InferenceResponse(
            body=response.json(),
            headers=response.headers,
            status_code=response.status_code,
            status_text=response.reason
        )

    def get(self, path: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None, timeout_seconds: Optional[int] = None) -> requests.Response:
        return self._make_request('GET', path, params=params, headers=headers, timeout_seconds=timeout_seconds)

    def post(self, path: str, json: Optional[Dict[str, Any]] = None, data: Optional[Union[str, Dict[str, Any]]] = None,
             params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None, timeout_seconds: Optional[int] = None) -> requests.Response:
        return self._make_request('POST', path, json=json, data=data, params=params, headers=headers, timeout_seconds=timeout_seconds)

    def put(self, path: str, json: Optional[Dict[str, Any]] = None, data: Optional[Union[str, Dict[str, Any]]] = None,
            params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None, timeout_seconds: Optional[int] = None) -> requests.Response:
        return self._make_request('PUT', path, json=json, data=data, params=params, headers=headers, timeout_seconds=timeout_seconds)

    def delete(self, path: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None, timeout_seconds: Optional[int] = None) -> requests.Response:
        return self._make_request('DELETE', path, params=params, headers=headers, timeout_seconds=timeout_seconds)

    def patch(self, path: str, json: Optional[Dict[str, Any]] = None, data: Optional[Union[str, Dict[str, Any]]] = None,
              params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None, timeout_seconds: Optional[int] = None) -> requests.Response:
        return self._make_request('PATCH', path, json=json, data=data, params=params, headers=headers, timeout_seconds=timeout_seconds)

    def head(self, path: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None, timeout_seconds: Optional[int] = None) -> requests.Response:
        return self._make_request('HEAD', path, params=params, headers=headers, timeout_seconds=timeout_seconds)

    def options(self, path: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None, timeout_seconds: Optional[int] = None) -> requests.Response:
        return self._make_request('OPTIONS', path, params=params, headers=headers, timeout_seconds=timeout_seconds)

    def health(self) -> dict:
        """
        Check the health status of the API.

        Returns:
            dict: Health status information

        Raises:
            InferenceClientError: If the health check fails
        """
        try:
            response = self.get('/health')
            return response.json()
        except InferenceClientError as e:
            raise InferenceClientError(f"Health check failed: {str(e)}")
