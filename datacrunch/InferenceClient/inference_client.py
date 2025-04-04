from dataclasses import dataclass
from dataclasses_json import dataclass_json, Undefined  # type: ignore
import requests
from requests.structures import CaseInsensitiveDict
from typing import Optional, Dict, Any, Union, Generator
from urllib.parse import urlparse


class InferenceClientError(Exception):
    """Base exception for InferenceClient errors."""
    pass


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class InferenceResponse:
    headers: CaseInsensitiveDict[str]
    status_code: int
    status_text: str
    _original_response: requests.Response
    _stream: bool = False

    def _is_stream_response(self, headers: CaseInsensitiveDict[str]) -> bool:
        """Check if the response headers indicate a streaming response.

        Args:
            headers: The response headers to check

        Returns:
            bool: True if the response is likely a stream, False otherwise
        """
        # Standard chunked transfer encoding
        is_chunked_transfer = headers.get(
            'Transfer-Encoding', '').lower() == 'chunked'
        # Server-Sent Events content type
        is_event_stream = headers.get(
            'Content-Type', '').lower() == 'text/event-stream'
        # NDJSON
        is_ndjson = headers.get(
            'Content-Type', '').lower() == 'application/x-ndjson'
        # Stream JSON
        is_stream_json = headers.get(
            'Content-Type', '').lower() == 'application/stream+json'
        # Keep-alive
        is_keep_alive = headers.get(
            'Connection', '').lower() == 'keep-alive'
        # No content length
        has_no_content_length = 'Content-Length' not in headers

        # No Content-Length with keep-alive often suggests streaming (though not definitive)
        is_keep_alive_and_no_content_length = is_keep_alive and has_no_content_length

        return (self._stream or is_chunked_transfer or is_event_stream or is_ndjson or
                is_stream_json or is_keep_alive_and_no_content_length)

    def output(self, is_text: bool = False) -> Any:
        try:
            if is_text:
                return self._original_response.text
            return self._original_response.json()
        except Exception as e:
            # if the response is a stream (check headers), raise relevant error
            if self._is_stream_response(self._original_response.headers):
                raise InferenceClientError(
                    f"Response might be a stream, use the stream method instead")
            raise InferenceClientError(
                f"Failed to parse response as JSON: {str(e)}")

    def stream(self, chunk_size: int = 512, as_text: bool = True) -> Generator[Any, None, None]:
        """Stream the response content.

        Args:
            chunk_size: Size of chunks to stream, in bytes
            as_text: If True, stream as text using iter_lines. If False, stream as binary using iter_content.

        Returns:
            Generator yielding chunks of the response
        """
        if as_text:
            for chunk in self._original_response.iter_lines(chunk_size=chunk_size):
                if chunk:
                    yield chunk
        else:
            for chunk in self._original_response.iter_content(chunk_size=chunk_size):
                if chunk:
                    yield chunk


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class AsyncInferenceExecution:
    _client: 'InferenceClient'
    id: str
    status: str  # TODO: add a status enum

    # TODO: Implement when the status endpoint is done
    def status(self) -> str:
        # Call the status endpoint and update the status when
        return self.status

    # TODO: Implement when the cancel inference execution endpoint is done
    # def cancel(self) -> None:
    #     pass

    # TODO: Implement when the results endpoint is done
    def get_results(self) -> Dict[str, Any]:
        pass
    # alias for get_results
    output = get_results


class InferenceClient:
    def __init__(self, inference_key: str, endpoint_base_url: str, timeout_seconds: int = 60 * 5) -> None:
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

    def run_sync(self, data: Dict[str, Any], path: str = "", timeout_seconds: int = 60 * 5, headers: Optional[Dict[str, str]] = None, http_method: str = "POST", stream: bool = False):
        response = self._make_request(
            http_method, path, json=data, timeout_seconds=timeout_seconds, headers=headers, stream=stream)

        return InferenceResponse(
            headers=response.headers,
            status_code=response.status_code,
            status_text=response.reason,
            _original_response=response
        )

    def run(self, data: Dict[str, Any], path: str = "", timeout_seconds: int = 60 * 5, headers: Optional[Dict[str, str]] = None, http_method: str = "POST"):
        # Add the "Prefer: respond-async" header to the request, to indicate that the request is async
        headers = headers or {}
        headers['Prefer'] = 'respond-async'

        response = self._make_request(
            http_method, path, json=data, timeout_seconds=timeout_seconds, headers=headers)

        # TODO: this response format isn't final
        execution_id = response.json()['id']

        return AsyncInferenceExecution(self, execution_id)

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

    def health(self, healthcheck_path: str = "/health") -> requests.Response:
        """
        Check the health status of the API.

        Returns:
            requests.Response: The response from the health check

        Raises:
            InferenceClientError: If the health check fails
        """
        try:
            return self.get(healthcheck_path)
        except InferenceClientError as e:
            raise InferenceClientError(f"Health check failed: {str(e)}")
