import pytest
from datacrunch.exceptions import APIException

ERROR_CODE = 'test_code'
ERROR_MESSAGE = "test message"


def test_api_exception_with_code():
    # arrange
    error_str = f'error code: {ERROR_CODE}\nmessage: {ERROR_MESSAGE}'

    # act
    with pytest.raises(APIException) as excinfo:
        raise APIException(ERROR_CODE, ERROR_MESSAGE)

    # assert
        assert excinfo.value.code == ERROR_CODE
        assert excinfo.value.message == ERROR_MESSAGE
        assert excinfo.value.__str__() == error_str


def test_api_exception_without_code():
    # arrange
    error_str = f'message: {ERROR_MESSAGE}'

    # act
    with pytest.raises(APIException) as excinfo:
        raise APIException(None, ERROR_MESSAGE)

    # assert
        assert excinfo.value.code is None
        assert excinfo.value.message == ERROR_MESSAGE
        assert excinfo.value.__str__() == error_str
