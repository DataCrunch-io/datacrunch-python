# Re-export Verda API for backwards compatibility

import warnings

from verda.verda import *  # noqa: F403
from verda.verda import VerdaClient as DataCrunchClient

warnings.warn(
    'datacrunch.datacrunch is deprecated; use `from verda` instead.',
    DeprecationWarning,
    stacklevel=2,
)
