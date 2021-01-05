class Actions:
    START = 'start'
    SHUTDOWN = 'shutdown'
    DELETE = 'delete'
    HIBERNATE = 'hibernate'
    RESTORE = 'restore'

    def __init__(self):
        return


class InstanceStatus:
    RUNNING = 'running'
    PROVISIONING = 'provisioning'
    OFFLINE = 'offline'
    STARTING_HIBERNATION = 'starting_hibernation'
    HIBERNATING = 'hibernating'
    RESTORING = 'restoring'
    ERROR = 'error'

    def __init__(self):
        return


class ErrorCodes:
    INVALID_REQUEST = "invalid_request"
    UNAUTHORIZED_REQUEST = "unauthorized_request"
    INSUFFICIENT_FUNDS = "insufficient_funds"
    FORBIDDEN_ACTION = "forbidden_action"
    NOT_FOUND = "not_found"
    SERVER_ERROR = "server_error"
    SERVICE_UNAVAILABLE = "service_unavailable"

    def __init__(self):
        return
