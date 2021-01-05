import time
from datacrunch.authentication.authentication import AuthenticationService
from datacrunch.balance.balance import BalanceService
from datacrunch.http_client.http_client import HTTPClient
from datacrunch.images.images import ImagesService
from datacrunch.instance_types.instance_types import InstanceTypesService
from datacrunch.instances.instances import InstancesService
from datacrunch.ssh_keys.ssh_keys import SSHKeysService
from datacrunch.startup_scripts.startup_scripts import StartupScriptsService
from datacrunch.constants import Actions, InstanceStatus, ErrorCodes
from datacrunch.__version__ import VERSION


class DataCrunchClient:
    """Client for interacting with DataCrunch's public API"""

    def __init__(self, client_id: str, client_secret: str, base_url: str = "https://api.datacrunch.io/v1") -> None:
        """The DataCrunch client

        :param client_id: client id 
        :type client_id: str
        :param client_secret: client secret
        :type client_secret: str
        :param base_url: base url for all the endpoints, optional, defaults to "https://api.datacrunch.io/v1"
        :type base_url: str, optional
        """
        self.actions = Actions()
        self.instance_status = InstanceStatus()
        self.error_codes = ErrorCodes()

        self.base_url = base_url
        self.version = VERSION

        self._authentication = AuthenticationService(
            client_id, client_secret, self.base_url)
        self._http_client = HTTPClient(self._authentication, self.base_url)
        self.balance = BalanceService(self._http_client)
        self.images = ImagesService(self._http_client)
        self.instance_types = InstanceTypesService(self._http_client)
        self.instances = InstancesService(self._http_client)
        self.ssh_keys = SSHKeysService(self._http_client)
        self.startup_scripts = StartupScriptsService(self._http_client)
