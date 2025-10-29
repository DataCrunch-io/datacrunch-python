import pytest

from datacrunch.exceptions import APIException

ERROR_CODE = 'test_code'
ERROR_MESSAGE = 'test message'


def test_api_exception_with_code():
    error_str = f'error code: {ERROR_CODE}\nmessage: {ERROR_MESSAGE}'

    with pytest.raises(APIException) as exc_info:
        raise APIException(ERROR_CODE, ERROR_MESSAGE)

    assert exc_info.value.code == ERROR_CODE
    assert exc_info.value.message == ERROR_MESSAGE
    assert exc_info.value.__str__() == error_str


def test_api_exception_without_code():
    error_str = f'message: {ERROR_MESSAGE}'

    with pytest.raises(APIException) as exc_info:
        raise APIException(None, ERROR_MESSAGE)

    assert exc_info.value.code is None
    assert exc_info.value.message == ERROR_MESSAGE
    assert exc_info.value.__str__() == error_str
