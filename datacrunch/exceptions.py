class APIException(Exception):
    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message

    def __str__(self) -> str:
        msg = ''
        if self.code:
            msg = f'error code: {self.code}\n'

        msg += f'message: {self.message}'
        return msg
