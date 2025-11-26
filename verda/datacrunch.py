# Frozen, minimal compatibility layer for old DataCrunch API

from verda import DataCrunchClient
from verda._version import __version__
from verda.authentication.authentication import AuthenticationService
from verda.balance.balance import BalanceService
from verda.constants import Constants
from verda.containers.containers import ContainersService
from verda.http_client.http_client import HTTPClient
from verda.images.images import ImagesService
from verda.instance_types.instance_types import InstanceTypesService
from verda.instances.instances import InstancesService
from verda.locations.locations import LocationsService
from verda.ssh_keys.ssh_keys import SSHKeysService
from verda.startup_scripts.startup_scripts import StartupScriptsService
from verda.volume_types.volume_types import VolumeTypesService
from verda.volumes.volumes import VolumesService

__all__ = [
    'AuthenticationService',
    'BalanceService',
    'Constants',
    'ContainersService',
    'DataCrunchClient',
    'HTTPClient',
    'ImagesService',
    'InstanceTypesService',
    'InstancesService',
    'LocationsService',
    'SSHKeysService',
    'StartupScriptsService',
    'VolumeTypesService',
    'VolumesService',
    '__version__',
]

import warnings

warnings.warn(
    'datacrunch.datacrunch is deprecated; use `from verda` instead.',
    DeprecationWarning,
    stacklevel=2,
)
