# Backwards compatibility

# Re-export the new API
from verda.verda import *

from verda.verda import VerdaClient as DataCrunchClient

import warnings
warnings.warn(
    "datacrunch.datacrunch is deprecated; use `from verda` instead.",
    DeprecationWarning,
    stacklevel=2,
)
