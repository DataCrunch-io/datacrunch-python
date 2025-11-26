# Compatibility layer for deprecated `datacrunch` package

from verda import (
    InferenceClient,
    __version__,
    authentication,
    balance,
    constants,
    containers,
    exceptions,
    helpers,
    http_client,
    images,
    instance_types,
    instances,
    locations,
    ssh_keys,
    startup_scripts,
    volume_types,
    volumes,
)
from verda import VerdaClient as DataCrunchClient

# For old `from datacrunch import *``
__all__ = [
    'DataCrunchClient',
    'InferenceClient',
    '__version__',
    'authentication',
    'balance',
    'constants',
    'containers',
    'datacrunch',
    'exceptions',
    'helpers',
    'http_client',
    'images',
    'instance_types',
    'instances',
    'locations',
    'ssh_keys',
    'startup_scripts',
    'volume_types',
    'volumes',
]

import warnings

warnings.warn(
    'datacrunch import is deprecated; use verda instead.',
    DeprecationWarning,
    stacklevel=2,
)
